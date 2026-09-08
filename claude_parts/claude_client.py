"""
All Claude API calls for the paper-upload tab live here. Two calls are used
as per the problem decomposition:

1. extract_paper_metadata(). This uses the cheap/fast model, reads ONLY the exam paper's
    cover page, returns just enough to build a dedup code (school, year,
    grade) plus three pre-processing facts (paper_number, paper_time, total_marks) that gate
    whether it is possible to proceed to the more credit heavy step. 

2. classify_paper(). The stronger model reads the exam paper AND the
    source text/insert, returns one classified row per question. Only ever
    called for papers that passed step 1's checks.

Only prelim (school-set) papers are handled. National/IEB papers are out of
scope as they will be checked again by me before being uploaded. 

Both PDFs are uploaded to Claude once via the Files API (upload_pdf) and referenced by
file_id in both calls where relevant.

"""

from __future__ import annotations

import streamlit as st
from anthropic import Anthropic

from claude_parts.taxonomy import (
    ALLOWED_SECTIONS,
    ALLOWED_SUBSKILLS,
    ALLOWED_TYPES,
    ADDITIONAL_NOTES,
    KEYWORD_GUIDANCE,
    MARKS_GUIDANCE,
    SECTION_DEFINITIONS,
    TYPE_DEFINITIONS,
    known_keyword_concepts_text,
)
from claude_parts.models import PaperAnalysis, PaperMetadata


EXTRACTION_MODEL = "claude-haiku-4-5-20251001"
CLASSIFICATION_MODEL = "claude-sonnet-5"

REFERENCE_CSV_PATH = "./data/paper_analysis_reference.csv"

# streamlit flow storage
@st.cache_resource
def get_client() -> Anthropic:
    return Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])


def upload_pdf(file_bytes: bytes, filename: str) -> str:
    """Uploads a PDF once via the Files API, returns its file_id for reuse
    across both the extraction and classification calls."""
    client = get_client()
    uploaded = client.files.upload(file=(filename, file_bytes, "application/pdf"))
    return uploaded.id


def _document_block(file_id: str) -> dict:
    return {"type": "document", "source": {"type": "file", "file_id": file_id}}


# ---------------------------------------------------------------------------
# Step 1: dedup-check extraction (cheap, small output, no source text needed)
# ---------------------------------------------------------------------------
# information of criteria for storage as JSON
_METADATA_TOOL = {
    "name": "record_paper_metadata",
    "description": (
        "Record identifying metadata for this exam paper, read from its "
        "cover page only. Every submitted paper is a school-set preliminary "
        "exam (never a national/IEB paper)."
    ),
    "input_schema": {  ## For future you can actually import criteria from the class definiton: .model_jason_schema()
        "type": "object",
        "properties": {
            "school_name": {
                "type": "string",
                "description": "The school's full name exactly as printed on the cover page."
                "OR IEB if the IEB logo is present.",
            },
            "year": {"type": "integer", "description": "Four-digit year, e.g. 2026."},
            "grade": {
                "type": "integer",
                "description": "The grade printed on the cover page, e.g. 12.",
            },
            "paper_number": {
                "type": "integer",
                "description": (
                    "The paper number printed on the cover page -- e.g. 1 for "
                    "'Paper I' or 'Paper 1'. Report exactly what's printed "
                    "even if it isn't 1; the caller decides what to do about it."
                ),
            "paper_time": {
                "type": "integer",
                "description": (
                    "The time taken to write the paper -- e.g 3 for 'Time: 3 hours"
                    "Report the number exactly as printed, even if it is not 3."
                    "The caller will decide what to do about it."
                )
            }
            },
            "total_marks": {
                "type": "integer",
                "description": "The total marks printed on the cover page, e.g. 100.",
            },
        },
        "required": ["school_name", "year", "grade", "paper_number", "paper_time", "total_marks"],
    },
}

# Claude API function
def extract_paper_metadata(exam_paper_file_id: str) -> PaperMetadata:
    client = get_client()
    response = client.messages.create(
        model=EXTRACTION_MODEL,
        max_tokens=300,
        tools=[_METADATA_TOOL],
        tool_choice={"type": "tool", "name": "record_paper_metadata"},
        messages=[
            {
                "role": "user",
                "content": [
                    _document_block(exam_paper_file_id),
                    {
                        "type": "text",
                        "text": (
                            "Read only the cover page of this exam paper and "
                            "call record_paper_metadata."
                        ),
                    },
                ],
            }
        ],
    )
    tool_use = next(b for b in response.content if b.type == "tool_use")
    return PaperMetadata.model_validate(tool_use.input)


# ---------------------------------------------------------------------------
# Step 2: full classification (only run for papers that passed step 1)
# ---------------------------------------------------------------------------
_CLASSIFY_TOOL = {
    "name": "record_paper_analysis",
    "description": "Record the classification of every question in this exam paper.",
    "input_schema": {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "Question number exactly as printed, e.g. '5.2.1'.",
                        },
                        "section": {"type": "string", "enum": ALLOWED_SECTIONS},
                        "type": {"type": "string", "enum": ALLOWED_TYPES},
                        "subskill": {"type": "string", "enum": ALLOWED_SUBSKILLS},
                        "keywords": {
                            "type": "string",
                            "description": (
                                "See the Keywords guidance in the system prompt. "
                                "For LF/DCQ/ICQ/VL: the specific named concept "
                                "(e.g. 'metaphor', 'concord', 'layout'), preferring "
                                "an existing label. For PU/C/Summary: a short "
                                "free-text cue phrase from the question."
                            ),
                        },
                        "question_total": {
                            "type": "integer",
                            "description": (
                                "Marks allocated to this specific question, e.g. "
                                "'(3)' printed next to it means 3. Not a section "
                                "subtotal."
                            ),
                        },
                    },
                    "required": [
                        "question",
                        "section",
                        "type",
                        "subskill",
                        "keywords",
                        "question_total",
                    ],
                },
            }
        },
        "required": ["questions"],
    },
}


def _load_reference_csv() -> str:
    with open(REFERENCE_CSV_PATH, "r", encoding="utf-8") as f:
        return f.read()


def _build_system_blocks() -> list[dict]:
    """One big cacheable block including the taxonomy + every historical classified
    paper, as few-shot grounding. Claude re-reads it from cache instead of
    reprocessing it for every new paper, which is most of the cost saving
    from doing this as a static reference rather than dynamic retrieval."""
    
    reference_csv = _load_reference_csv()

    text = f"""You are classifying questions from a South African NSC/IEB
    English Home Language Paper I exam paper into a structured taxonomy, for a
    teacher building a longitudinal dataset of question patterns across years.

    ## Sections

    {SECTION_DEFINITIONS}

    ## Types

    {TYPE_DEFINITIONS}

    ## Subskills

    Every question must be tagged with exactly one subskill from this fixed list
    -- do not invent new ones: {", ".join(ALLOWED_SUBSKILLS)}

    {ADDITIONAL_NOTES}

    ## Keywords

    This is the trickiest column. {KEYWORD_GUIDANCE}

    Known concept dictionary (Type: comma-separated known concepts), current as
    of the last time this list was refreshed from the historical data:

    {known_keyword_concepts_text()}

    ## Marks

    {MARKS_GUIDANCE}

    ## Worked examples: every question from the last several years, already classified

    Use this as your primary guide for borderline calls -- when a new question
    closely resembles one below, classify it the same way, keywords included.
    Format is ID,Question,Section,Type,Subskill,Keywords,QuestionTotal (ID is the
    paper code from the historical national papers this taxonomy was originally
    built on, ignore it. It's not relevant to classifying the new school prelim
    paper).

    {reference_csv}

    ## Task

    You will be given a new exam paper (and, where relevant, its accompanying
    source-text Insert). Classify every question in Section 1 through the end of
    Section 6, in order, one row per question/sub-question exactly as numbered in
    the paper (e.g. '5.2.1', not '5.2'), including its question_total. Call
    record_paper_analysis once with the complete list."""

    return [{"type": "text", "text": text, "cache_control": {"type": "ephemeral", "ttl": "1h"}}]


def classify_paper(exam_paper_file_id: str, source_text_file_id: str) -> PaperAnalysis:
    client = get_client()
    response = client.messages.create(
        model=CLASSIFICATION_MODEL,
        max_tokens=4096,
        system=_build_system_blocks(),
        tools=[_CLASSIFY_TOOL],
        tool_choice={"type": "tool", "name": "record_paper_analysis"},
        messages=[
            {
                "role": "user",
                "content": [
                    _document_block(exam_paper_file_id),
                    _document_block(source_text_file_id),
                    {
                        "type": "text",
                        "text": (
                            "Here is the new exam paper and its source-text "
                            "Insert. Classify every question and call "
                            "record_paper_analysis."
                        ),
                    },
                ],
            }
        ],
    )
    tool_use = next(b for b in response.content if b.type == "tool_use")
    return PaperAnalysis.model_validate(tool_use.input)
