"""
Uploads a prelim exam paper + its source-text.
Inserts and preforms a dedup check against the registry, validates it's a genuine Paper 1
worth 100 marks, classifies, stores. Powered by Anthropic SDK and API.

Only prelim (school-set) papers are handled here. No national/IEB papers
are expected, so there's no paper-type branching anywhere in this flow.

This runs synchronously in a single pass on the button click: there's no longer a
step that needs to pause and wait for a person, so there's no multi-stage
session_state machine to manage.

"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from claude_parts import db

from claude_parts.claude_client import classify_paper, extract_paper_metadata, upload_pdf


EXPECTED_PAPER_NUMBER = 1
EXPECTED_TOTAL_MARKS = 100

CSV_COLUMNS = ["question", "section", "type", "subskill", "keywords", "question_total", "count"]


def _build_paper_code(metadata, school_code_prefix: str) -> str:
    return f"{school_code_prefix}{metadata.year}G{metadata.grade}"


def render_paper_upload_tab() -> None:
    st.subheader("Upload a new paper for analysis")
    st.write(
        "Upload an examination question paper and its source-text (or any English Paper 1 with the IEB structure). "
        "The uploads must be in a pdf format. If your paper has not already been analysed, this tool will classify " \
        "the question types and concepts in your paper and generate a new paper code. You can " \
        "then select your paper code in the reflection tab and produce a report on your results for that specific paper. "
    )

    col1, col2 = st.columns(2)
    with col1:

        exam_pdf = st.file_uploader("Exam question paper (PDF)", type="pdf", key="exam_pdf_upload", accept_multiple_files=False)

    with col2:
        source_pdf = st.file_uploader("Source text / Insert (PDF)", type="pdf", key="source_pdf_upload", accept_multiple_files=False)

    analyze_clicked = st.button(
        "Analyse paper", type="primary", disabled=not (exam_pdf and source_pdf)
    )

    # crucial for streamlit updating.
    if not analyze_clicked:
        return

    
    try:
        with st.spinner("Uploading and checking your paper... "):
            exam_file_id = upload_pdf(exam_pdf.getvalue(), exam_pdf.name)
            source_file_id = upload_pdf(source_pdf.getvalue(), source_pdf.name)
            metadata = extract_paper_metadata(exam_file_id)
    except Exception as e:
        st.error(f"Couldn't read the paper's metadata.")
        return

    school_code_prefix = db.get_or_create_school_code(metadata.school_name)
    paper_code = _build_paper_code(metadata, school_code_prefix)

    # 1. Dedup: has this school/year/grade combination already been analysed?
    if db.paper_exists(metadata.school_name, metadata.year, metadata.grade):
        st.warning(
            f"A paper for '{metadata.school_name}', {metadata.year}, grade "
            f"{metadata.grade} has already been analysed. The paper code is: ('{paper_code}'). You can already find it in the reflection tab."
        )
        existing = db.get_analysis(paper_code)
        if existing:
            st.dataframe(pd.DataFrame(existing), use_container_width=True)
        return

    # 2. Pre-check: must be Paper 1, worth 100 marks, before we spend a
    #    classification call on it.
    problems = []
    if metadata.paper_number != EXPECTED_PAPER_NUMBER:
        problems.append(
            f"this is Paper {metadata.paper_number}, not Paper {EXPECTED_PAPER_NUMBER}"
        )
    if metadata.total_marks != EXPECTED_TOTAL_MARKS:
        problems.append(
            f"the cover page states {metadata.total_marks} total marks, "
            f"not {EXPECTED_TOTAL_MARKS}"
        )

    if metadata.school_name == 'IEB' or metadata.school_name == 'ieb': # comment out to analyse IEB papers
        problems.append(
        f'this is an IEB examination not a school prelim examination.'
    )
        
    if metadata.paper_time != 3:
        problems.append(
            'this paper is not a full 3 hour paper.'
        )

    if problems:
        st.error("This paper doesn't meet the requirements for analysis:")
        return

    # 3. Classify.
    try:
        with st.spinner(f"Approved with paper code: '{paper_code}'. Classifying..."):
            analysis = classify_paper(exam_file_id, source_file_id)
    except Exception as e:
        st.error(f"Classification failed. No API credit remaining.")
        return

    rows = [q.model_dump() for q in analysis.questions]
    for row in rows:
        row["count"] = 1
    df = pd.DataFrame(rows, columns=CSV_COLUMNS)
    marks_sum = sum(row["question_total"] for row in rows)

    db.register_paper(
        paper_code=paper_code,
        school_name=metadata.school_name.capitalize(),
        year=metadata.year,
        grade=metadata.grade,
        paper_number=metadata.paper_number,
        total_marks=metadata.total_marks,
    )
    db.save_analysis(paper_code, rows)

    st.success(f"Your paper has been uploaded. The paper code is: {paper_code}.")

    if marks_sum != metadata.total_marks:
        st.warning(
            f"The extracted question marks sum to {marks_sum}, but the cover "
            f"page states {metadata.total_marks}. Worth a manual check."
            f"The paper will be saved anyway."
        )

    st.dataframe(df[["question", "section", "type", "keywords", "question_total"]], use_container_width=True, hide_index=True)
