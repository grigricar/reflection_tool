import streamlit as st
import os
import pandas as pd
import plotly.express as px
from views.reflection_tool import reflection_tool
from views.q_type import q_type
from views.insights import insights

# settings
#hides input bin messages
st.markdown(
    """
    <style>
    div[data-testid="InputInstructions"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# VISUAL SETUP
tab1, tab2, tab3 = st.tabs(["Definitions", "Reflection Tool", "Insights" ])

with tab1:
    q_type()

with tab2:
    data_path = "data/no_bloom.pkl"
    reflection_tool(data_path)

with tab3:
    data_source = "data/no_bloom.pkl"
    insights(data_source)


# Sidebar Info
st.sidebar.header('E_h Reflective Tool 👁️', divider= 'green')

st.sidebar.caption("Recalibrate your approach to English Paper 1!")


st.sidebar.markdown("Created by [Greg Carter](https://www.linkedin.com/in/gregory-carter-786813325)")

st.sidebar.header('', divider='green')

with st.sidebar.expander("Quick Definitions:"):
    st.markdown("**Direct Concept Question (DCQ):** \n" \
    "Direct mention of a concept the question wants you to focus on and apply.")

    st.markdown("**Indirect Concept Question (ICQ):** \n" \
    "The identification of a concept(s) is required by the question.")

    st.markdown("**Visual Lit (VL):** \n" \
        "The dominant focus is visual interpretation.")

    st.markdown("**Pure Understanding(PU):** \n" \
        "Direct engagement with meaning and argument.")

    st.markdown("**Language Focused (LF):** \n" \
        "Mechanics of English: parts of speech, syntax, sentence structure, punctuation, errors.")

    st.markdown("**Comparative(C):** \n" \
        "Technique of comparing one source to another.")

    st.markdown("**Summary:** \n" \
        "Synthesis of sources into a new style.")

st.sidebar.header('', divider='green')

st.sidebar.text("Use the search in the table below to find specific question types in papers:")
data_search = pd.read_pickle("data/no_bloom.pkl")
data_search = data_search[['ID', 'Question', 'Type']]

with st.sidebar.expander("Question Search:"):
    st.dataframe(data_search, hide_index=True)

st.sidebar.link_button("ACCESS IEB past papers", 'https://www.ieb.co.za/assessment/high-schools/national-senior-certificate/nsc-past-papers')