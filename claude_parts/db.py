"""
Supabase layer for the paper-upload tab.

"""

from __future__ import annotations

import re

import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase_client() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# Words dropped when auto-generating a code prefix from a school's name 
# generic institutional words that don't help distinguish one school from
# another 

_CODE_FILLER_WORDS = {
    "college", "school", "high", "secondary", "academy", "primary",
    "combined", "the", "of", "and",
}
# ---------------------------------------------------------------------------
# schools -- prelim school name -> code prefix lookup
# ---------------------------------------------------------------------------

def find_school(school_name: str) -> dict | None:
    """Exact-match lookup. Names are messy in the wild (typos, 'St' vs 'St.'),
    so this deliberately does NOT fuzzy-match -- a near-miss should surface as
    a "new school" prompt rather than silently attach to the wrong one."""
    client = get_supabase_client()
    res = (
        client.table("schools")
        .select("*")
        .eq("school_name", school_name)
        .execute()
    )
    return res.data[0] if res.data else None


def add_school(school_name: str, code_prefix: str) -> None:
    client = get_supabase_client()
    client.table("schools").insert(
        {"school_name": school_name.title(), "code_prefix": code_prefix.upper()}
    ).execute()


def code_prefix_exists(code_prefix: str) -> bool:
    client = get_supabase_client()
    res = client.table("schools").select("id").eq("code_prefix", code_prefix).execute()
    return len(res.data) > 0


# (e.g. "St Stithians Boys College" -> initials of "St", "Stithians",
# "Boys" -> "SSTB", not "St Stithians Boys College" -> "SSBC").

def _initials_from_school_name(school_name: str) -> str:
    """'St Stithians Boys College' -> 'SSB'. Drops generic filler words, then
    takes the first letter of each remaining word with two from the 
     second word. (or, if only one significant word survives: e.g. 'Roedean School',
    its first three letters, so a single-word name doesn't collapse to one character).
    This is a mechanical rule, not a judgment call. It won't always land on the
    abbreviation a human would pick (e.g. it can't know to drop a word like
    'Marist' the way you might), but it's deterministic and never needs a
    person in the loop."""
    words = [w for w in re.split(r"\s+", school_name.strip()) if w]
    significant = [w for w in words if w.strip(".,'").lower() not in _CODE_FILLER_WORDS]
    if not significant:
        significant = words  # every word was filler -- fall back to all of them
    if len(significant) == 1:
        return significant[0][:3].upper() or "SCH"
    letters = "".join(
        w[:2].upper() if i == 1 else w[0].upper()
        for i, w in enumerate(significant)
        if w[0].isalpha()
)
    
    return letters[:5] or "SCH"


# def _generate_unique_code_prefix(school_name: str) -> str:
#     """Appends a numeric suffix on collision (two schools whose initials
#     happen to match) so code_prefix -- and therefore every paper code built
#     from it -- stays unique without ever asking a person to intervene."""
#     base = _initials_from_school_name(school_name)
#     candidate = base
#     suffix = 2
#     while code_prefix_exists(candidate):
#         candidate = f"{base}{suffix}"
#         suffix += 1
#     return candidate


def get_or_create_school_code(school_name: str) -> str:
    """The single entry point paper_upload_tab.py calls: returns the code
    prefix for this school, transparently registering the school with an
    auto-generated code the first time it's seen. Never prompts a person."""
    existing = find_school(school_name)
    if existing:
        return existing["code_prefix"]
    code_prefix = _initials_from_school_name(school_name) #_generate_unique_code_prefix(school_name)
    add_school(school_name, code_prefix)
    return code_prefix

# def pdf_to_storage(file_bytes: bytes, filename: str) -> str:
#     """Uploads a PDF to Supabase Storage, returns the path it was stored at."""
#     path = f"papers/{filename}"  # folder-like prefix inside the bucket
#     client = get_supabase_client()
#     client.storage.from_("papers").upload(
#         path,
#         file_bytes,
#         file_options={"content-type": "application/pdf"}
#     )
#     return path
# ONLY USED IF PAPERS ARE STORED. AVOID AS THIS BREACHES COPYRIGHT.

# ---------------------------------------------------------------------------
# papers -- the dedup registry (step 2 of the pipeline)
# ---------------------------------------------------------------------------

def paper_exists(school_name: str, year: int, grade: int) -> bool:
    """The dedup check, per your instruction: matched on school + year +
    grade directly (not on the generated code) -- if a row matches, this
    paper has already been analysed."""
    client = get_supabase_client()
    res = (
        client.table("papers")
        .select("code")
        .eq("school_name", school_name)
        .eq("year", year)
        .eq("grade", grade)
        .execute()
    )
    return len(res.data) > 0


def register_paper(
    paper_code: str,
    school_name: str,
    year: int,
    grade: int,
    paper_number: int,
    total_marks: int,
) -> None:
    client = get_supabase_client()
    client.table("papers").insert(
        {
            "code": paper_code,
            "school_name": school_name.title(),
            "year": year,
            "grade": grade,
            "paper_number": paper_number,
            "total_marks": total_marks,
        }
    ).execute()


# ---------------------------------------------------------------------------
# paper_questions -- the analysis itself
# ---------------------------------------------------------------------------

def save_analysis(paper_code: str, rows: list[dict]) -> None:
    """rows: list of {"question", "section", "type", "subskill", "keywords",
    "question_total", "count"}. "count" is expected to already be set to 1 by
    the caller -- it's never something Claude produces."""
    client = get_supabase_client()
    payload = [{**row, "paper_code": paper_code} for row in rows]
    client.table("paper_questions").insert(payload).execute()


def get_analysis(paper_code: str):
    """Returns the stored analysis for one paper as a list of dicts, ordered
    the way they were saved. Used for re-downloading a CSV and, later, by
    your reflection tool tab."""
    client = get_supabase_client()
    res = (
        client.table("paper_questions")
        .select("question,section,type,subskill,keywords,question_total,count")
        .eq("paper_code", paper_code)
        .order("id")
        .execute()
    )
    return res.data
