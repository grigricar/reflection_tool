"""
Pydantic models used to validate what Claude's tool calls return, before uploading 
to the database. If Claude's output doesn't fit these
shapes, you want a clear validation error here -- not a malformed row quietly
landing in Supabase.

"""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field

from claude_parts.taxonomy import ALLOWED_SECTIONS, ALLOWED_TYPES, ALLOWED_SUBSKILLS


# ---------------------------------------------------------------------------
# Step 1 (dedup check + pre-flight validation). Includes what the cheap extraction
# call must return. Only prelim (school-set) papers are ever submitted here
# (no national/IEB papers) so this is deliberately simple: every field is
# always required, there's no paper_type branching.
# ---------------------------------------------------------------------------
class PaperMetadata(BaseModel):
    school_name: str = Field(min_length=1)
    year: int = Field(ge=2000, le=2100)
    grade: int = Field(ge=8, le=12)
    paper_number: int = Field(ge=1, description="e.g. 1 for 'Paper I'/'Paper 1'")
    total_marks: int = Field(ge=1, description="Total marks printed on the cover page")
    paper_time: int = Field(ge=1, description= "Time allowed for writing the paper")


# ---------------------------------------------------------------------------
# Step 2 (classification) -- what the full analysis call must return
# ---------------------------------------------------------------------------
class QuestionRow(BaseModel):
    question: str
    section: Literal[tuple(ALLOWED_SECTIONS)]  # type: ignore[valid-type]
    type: Literal[tuple(ALLOWED_TYPES)]  # type: ignore[valid-type]
    subskill: Literal[tuple(ALLOWED_SUBSKILLS)]  # type: ignore[valid-type]
    # unlike Subskill, Keywords is allowed to grow (new concepts can get coined).
    # See taxonomy.py's KEYWORD_GUIDANCE and is_known_keyword(). New coinages are flagged for
    # review in the UI, not rejected here.
    keywords: str = Field(min_length=1)
    question_total: int = Field(ge=1, description="Marks allocated to this question")


class PaperAnalysis(BaseModel):
    questions: list[QuestionRow]
