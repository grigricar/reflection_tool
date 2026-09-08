"""
Classification taxonomy for NSC/IEB English Home Language Paper I analysis.

This all flows straight into the system prompt built in claude_client.py.


"""

# ---------------------------------------------------------------------------
# SECTION -- which part of the paper a question belongs to.
# One question paper always has these six sections, in this order.
# ---------------------------------------------------------------------------
ALLOWED_SECTIONS = ["Comp", "Summary", "Seen", "Unseen", "Crit", "Lang"]

SECTION_DEFINITIONS = """
- Comp (Question 1, Comprehension): Questions on a single non-fiction/opinion
  passage (TEXT 1 in the Insert). Usually 7-9 sub-questions of increasing
  difficulty, the last of which is often a comparative question (Type C)
  linking TEXT 1 to a poem printed directly in the question paper.
- Summary (Question 2): Always exactly one question, always Type=Summary,
  Subskill=synthesis. Summarise TEXT 1 (or a related text) in a fixed word
  count.
- Seen (Question 3, Seen Poem): Questions on a poem the class studied in
  advance (a prescribed/anthology poem named in the paper).
- Unseen (Question 4, Unseen Poem): Questions on a poem the candidates have
  not encountered before.
- Crit (Question 5, Critical Reading): Questions on a second Insert text or
  set of texts (TEXT 2A/2B etc.), often mixing a written passage with a
  visual element (a cartoon, infographic or advertisement) -- this is where
  most VL (Visual Literacy) questions appear, alongside LF/DCQ/ICQ/PU/C items.
- Lang (Question 6, Language): Editing/grammar-in-context questions on a
  short passage -- punctuation, sentence structure, concord, tenses, register
  etc. Dominated by Type=LF.
""".strip()

# ---------------------------------------------------------------------------
# TYPE -- copied verbatim from question_type_classification.rtf
# ---------------------------------------------------------------------------
ALLOWED_TYPES = ["DCQ", "ICQ", "LF", "PU", "C", "VL", "Summary"]

TYPE_DEFINITIONS = """
- DCQ (Direct Concept Question): These questions direct mention of a concept the question wants you to focus on in the question itself. These can be figures of speech, but can also
  include other concepts from style such as diction and intention, and concepts particular to poetry (eg. enjambment). On the whole, these are quite
  easy questions to improve in. The concepts are directly mentioned in these questions types and you are asked to apply them. The most challenging 
  version of this question comes in the form of explaining or arguing about the existence of the concept itself (eg. Argue if the phrase is an example of 
  ambiguity or ambivalence).
- ICQ (Indirect Concept Question): Concept is tested implicitly. This question type also tests for a concept, but here the student is expected 
  to identify the concept, or use a combination of concepts implied by the question in their answer (i.e in tone questions it is usually
  implied that you use another concepts, diction or rhythm, to support your answer). These questions can be more open-ended.
  Another notorious examples are vague questions concerning 'imagery' which can be answered by using many types of figures of speech.
  These questions place the burden on the student to identify, find and apply concepts. Often the referred to source and lines 
  will need to be considered to confirm the concept expected.  
- LF (Language Focused): Pure grammar, syntax, parts of speech, punctuation,
  or usage. These are pure language and grammar skill questions. The mechanics, the nuts and bolts of English include: 
  parts of speech, syntax, sentence structure, punctuation. They can connect to style but the core is
  language knowledge. Some of them can be very niche and require specific word knowledge (eg. apart vs a part). 
  The majority are in fact extremely predictable (e.g: active vs passive, initialism vs acronym, your vs you're).
- PU (Pure Understanding): Demands own-words explanation. These questions force the student to engage directly with meaning and
  show that they understand ideas in their own words. The key skills are vocabulary and ability to infer meaning.
  These types of questions can also focus on argumentation and picking up on a writer's logic, as opposed to applying any 
  technical concept learnt.
- C (Comparative): Multi-text or text-to-image comparisons. Usually placed at the end of sections.
  Students are required to compare one text/image/poem to one or more other sources. They usually have high mark allocations (4-5).
  They are quite open ended and sometimes refer to multiple concepts. They are often prefaced by use of the word 'critically', and 
  contain other signal words like 'discuss' or 'fully discuss' or 'explore'; sometimes 'argue'.
- VL (Visual Lit): Interpretation of images, cartoons, film techniques, or
  layouts. These questions are distinguished from concept questions because visual literacy
  questions involve a different skill set with differing concepts. Here we are talking interpretation of images frequently involving
  advertising, cartoons, and film technique. Often mostly part of the critical literacy sections but not always.
- Summary: Standard summary synthesis questions (Question 2 only. Always 10 marks.).
""".strip()

# ---------------------------------------------------------------------------
# SUBSKILL -- controlled vocabulary, extracted from paper_analysis_reference.csv
# New papers are constrained to this list (per your "constrain to existing
# values" choice). If a genuinely new subskill shows up, add it here first,
# then re-run the analysis -- don't let Claude invent new labels on the fly,
# to keep the column consistent over time.
# ---------------------------------------------------------------------------
ALLOWED_SUBSKILLS = [
    "apply definition",
    "argumentation",
    "cartoon",
    "comparative",
    "diction",
    "error",
    "fos",
    "inference",
    "language",
    "mixed",
    "opinion",
    "punctuation",
    "rhythm",
    "sentence structure",
    "sound device",
    "structure",
    "style",
    "synthesis",
]

# Add any free-text notes/sub-rules you haven't put in writing anywhere else
# yet -- e.g. "fos" = "figures of speech", edge cases between PU and ICQ, etc.
# This block gets appended to the system prompt as-is.
ADDITIONAL_NOTES = """
- "fos" = figures of speech.
- "mixed" is used when a single question spans more than one subskill and no
  single label dominates (common on the final comparative question of a
  section).
""".strip()

# ---------------------------------------------------------------------------
# KEYWORDS -- the "which specific concept" column, added after the rest of
# this taxonomy was built. Deliberately open-ended rather than a closed enum:
# most questions should match an existing concept below, but a genuinely new
# one (a device/rule not seen before) should get a new, concisely-labelled
# entry rather than being forced into the nearest existing tag.
#
# KEYWORD_CONCEPTS is only meaningful for Types LF, DCQ, ICQ, VL -- for those,
# it names the specific grammatical/literary/visual concept being tested
# (e.g. "metaphor", "concord", "layout"). It was extracted programmatically
# from paper_analysis_reference.csv, grouped by Type. For Types PU, C and
# Summary, Keywords is free-text describing what's distinctive about the
# question (see the worked examples in the reference CSV) -- there's no
# vocabulary to maintain for those.
# ---------------------------------------------------------------------------
CONCEPT_TYPES = ["LF", "DCQ", "ICQ", "VL"]

KEYWORD_CONCEPTS: dict[str, list[str]] = {
    "LF": [
        "acronym", "active/passive voice", "apostrophe", "colon", "comma splice",
        "commas", "concord", "dash", "direct/indirect/reported speech", "ellipsis",
        "evaluate effectiveness (two sentences)", "full sentence", "hyphen",
        "imperative declarative iterrogative", "initialism", "interjection",
        "inverted commas", "italics", "loose vs periodic", "main/subordinate clause",
        "malapropism", "misrelated participle", "morphology", "neologism",
        "parenthesis", "pronouns", "rhetorical questions", "rhythm", "semi-colon",
        "simple compound complex", "split infinitive", "subject verb object",
        "synonym", "tautology", "word confusion", "word skill",
    ],
    "DCQ": [
        "alliteration", "anecdote", "cliché", "enjambment", "euphemism",
        "hyperbole", "intention/tone/diction", "irony", "juxtaposition",
        "literal and figurative", "metaphor", "paradox", "personification",
        "pun", "register", "satire", "simile", "sound device", "synecdoche",
    ],
    "ICQ": [
        "enjambment", "figure of speech", "form + structure", "imagery",
        "line structure", "repetition", "rhythm", "shift + style/tone",
        "style", "typography",
    ],
    "VL": [
        "colour and/or font", "hashtag", "infographic", "irony", "layout",
        "propaganda", "slogan", "values/message/interests/impact",
        "visual + verbal details", "visual metaphor/pun", "visual only",
    ],
}

KEYWORD_GUIDANCE = """
For Type in (LF, DCQ, ICQ, VL): the Keywords field names the SPECIFIC concept
being tested -- not the general Subskill category, but the exact device or
rule (e.g. Subskill=fos, Keywords=metaphor; Subskill=punctuation,
Keywords=colon). The concept is usually named or clearly implied by the
question's own wording. When it isn't, refer to the source text the question
points to (the specific line/paragraph/image referenced) to identify it.
Prefer an existing label from the concept dictionary below when the question
matches one -- reuse the exact same wording/casing so the same concept is
never tagged two different ways. Only when a question tests a concept that
genuinely isn't covered below, coin a new label: concise (1-3 words),
lowercase, in the same style as the existing ones. For the question types
LF, DCQ, ICQ, VL: keyword classification can only have one concept item. There
can be no commas listing other concepts or question words.

For Type in (PU, C, Summary): Keywords is a short free-text tag (a handful of
comma-separated cue words or phrases from the question) capturing what's
distinctive about this specific question -- not a controlled vocabulary.
Match the style shown in the worked examples below.
""".strip()


def known_keyword_concepts_text() -> str:
    """Renders KEYWORD_CONCEPTS as a readable block for the system prompt."""
    lines = []
    for type_code, concepts in KEYWORD_CONCEPTS.items():
        lines.append(f"{type_code}: " + ", ".join(concepts))
    return "\n".join(lines)

# Dropped from use as user input could be used irresponsibly
def is_known_keyword(type_code: str, keyword: str) -> bool:
    """False only for a genuinely new concept on one of the four concept
    types -- used by the UI to flag new coinages for review, not to
    block them. PU/C/Summary keywords are always considered 'known' since
    they were never a controlled vocabulary to begin with."""
    if type_code not in KEYWORD_CONCEPTS:
        return True
    known = {k.lower() for k in KEYWORD_CONCEPTS[type_code]}
    return keyword.strip().lower() in known


# ---------------------------------------------------------------------------
# MARKS -- the "Question Total" column, added alongside Keywords.
# ---------------------------------------------------------------------------
MARKS_GUIDANCE = """
Record question_total as the mark allocation printed in brackets immediately
after each question/sub-question, e.g. '(3)' means question_total=3. Use the
mark for the specific sub-question being classified, not a running or section
subtotal -- section totals printed in square brackets at the end of a
question (e.g. '[25]') are NOT a question_total for any individual row, they
only exist to sanity-check your own arithmetic.
""".strip()
