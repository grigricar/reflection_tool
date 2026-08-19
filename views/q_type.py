import pandas as pd
import plotly.express as px
import streamlit as st
import os


def q_type():

    st.image(os.path.join(os.getcwd(), "static", "header2.png"))
    st.page_link(page="https://www.youtube.com/channel/UCCDNh1fC2C93zzyIj15fC0g", label="An @English_hacked reflective tool")

    st.title("Question Types")
    st.text("Improving your Paper I mark can feel like trying to hit a moving target. Where do you even begin? This reflective tool gives you a clear starting point by " \
    "helping you focus on question types rather than individual sections. You'll discover that some questions are far more predictable, and therefore " \
    "easier to prepare for, than others. \n" 
    "\n"
    "Across Paper 1 there are many repeatable question types. For example, on average, Language Focused (LF) questions account for 20% of the paper! " \
    "These questions are not by any means restricted to the final 'Language Section'. \n " \
    "\n" \
    "Knowing where your strengths lie in answering these different question types " \
    "can help you to target weaker areas in an alternative way. The definitions provided below are an attempt to define question types that occur across sections. " \
    "These definitions can be somewhat fuzzy and there is room to debate them, but after considered analysis of papers the definitions below appear to be a robust " \
    "framework to improve paper reflection and discover where best to allocate your study time and focus. \n " \
    "\n" \
    "Navigate to the 'Reflection Tool' in the tabs above to enter your results for examination papers from 2020 to 2025 to generate a report that will help you identify " \
    "which question types you need to work on most. ")

    new_map = {
                    'C': "Comparative",
                    'DCQ':"Direct Concept Question",
                    'ICQ':"Indirect Concept Question",
                    'LF':"Language Focused",
                    'PU':"Pure Understanding",
                    'Summary':"Summary",
                    'VL': "Visual Literacy",
        }
        #remapping and grouping data
    paper_eda = pd.read_pickle('data/no_bloom.pkl')
    paper_eda['Type'] = paper_eda['Type'].map(new_map)
    paper_id_type_sort = paper_eda.groupby(["ID", "Type"])['Question Total'].sum().reset_index()
    avg_questions = paper_id_type_sort.groupby('Type')['Question Total'].mean().round(2).reset_index().sort_values('Question Total')

    #Donut for avg. question type % in papers 
    fig = px.pie(
    avg_questions,
    values="Question Total",       
    names="Type",    
    title="Average Percentage of Marks in Paper 1 by Question Type",
    color_discrete_sequence=px.colors.qualitative.Set2,  
    hole = 0.4
    )

    fig.update_layout(
    legend=dict(
        title= dict(text='Question Types:\n\n' \
        '\n', font=dict(size=16)),
        x=-0.3,        
        y=1,           
        xanchor="left",  
        yanchor="top"
    ),
    margin=dict(l=120, r=20, t=60, b=20) # Expands pie area and reserves left space for legend
)

    fig.update_traces(
    insidetextfont=dict(
        weight="bold",
        size=14  # Optional: increase font size for better readability
    )
)

    st.plotly_chart(fig, width='stretch')

    qtype_avg = dict(zip(avg_questions['Type'], (round(avg_questions['Question Total']))/100))

    st.divider()

    st.title("Definitions")

    with st.container(border=True):
        st.subheader("Direct Concept Question (DCQ):")
        st.metric(label= "Average % of marks in P1:", value= qtype_avg['Direct Concept Question'], format='percent')
        st.text("These involve direct mention of a concept the question wants you to focus on. These can be figures of speech, but can also " \
        " include other concepts from style such as diction and intention, and concepts particular to poetry (eg. enjambment). On the whole, these are quite"
        " easy questions to improve in. The concepts are directly mentioned in these questions types and you are asked to apply them. The most challenging " \
        " version of this question comes in the form of explaining or arguing about the existence of the concept itself (eg. Argue if the phrase is an example of" \
        " ambiguity or ambivalence.)  " )

        expand = st.expander("Example 1")
        expand.markdown("(2025NOV, Q4.4) \n" \
        "\n" \
        "Refer to lines 13-16: \n 'A miracle of … satisfied, Nature's call.' \n " \
        "\n " \
        "Discuss how the **alliteration** highlights the relationship between the rain and nature. (3)")

        expand = st.expander("Example 2")
        expand.markdown("(2025NOV, Q5.2.2) \n" \
                    "\n" \
                    "Explain whether the figure of speech used **is clichéd**. (3)")
        
    with st.container(border=True):
            st.subheader("Indirect Concept Question (ICQ):")
            st.metric(label= "Average % of marks in P1:", value= qtype_avg['Indirect Concept Question'], format='percent')
            st.text("This question type also tests for a concept, but here you are excepted to identify the concept "
            "or use a combination of concepts implied by the question in your answer (i.e in tone questions it is usually " \
            "implied that you use another concepts, diction or rhythm, to support your answer). These can be more open-ended. " \
            "Another notorious example are vague questions concerning 'imagery' which can be answered by using many types of figures of speech. " \
            " Generally, these questions are harder, but can still easily be prepared for.   " )
    
            expand = st.expander("Example 1")
            expand.markdown("(2025NOV, Q1.6) \n" \
            "\n" \
            "Refer to paragraph 7. \n " \
            "\n " \
            "**Identify the figure of speech** in 'Meaning, like beauty, is subjective' and comment " \
            "on its effectiveness in the context of paragraph 7. (3)")
    
            expand = st.expander("Example 2")
            expand.markdown("(2025NOV, Q5.1) \n" \
                        "\n Consider the following from TEXT 5A."
                        "\n" \
                        "\n Discuss how **the verbal details** reinforce the importance of Sunitha Krishnan's " \
                        "work. (3) ")
            
    with st.container(border=True):
        st.subheader("Visual Lit (VL):")
        st.metric(label= "Average % of marks in P1:", value= qtype_avg['Visual Literacy'], format='percent')
        st.text("These questions are distinguished from concept questions because visual literacy "\
                "questions involve a different skill set with differing concepts. Here we are talking interpretation of images frequently involving " \
                "advertising, cartoons, and film technique. Often mostly part of the critical literacy sections but not always." )
        
        expand = st.expander("Example 1")
        expand.markdown("(2025NOV, Q5.4) \n" \
        "\n" \
        "Refer to TEXT 5B. \n " \
        "\n " \
        "Discuss whether **the layout** of the advertisement is effective in portraying the horrific nature of human trafficking. " \
        "Refer to **the placement** of **specific visual** and verbal details in it to support your response. (4) " )

        expand = st.expander("Example 2")
        expand.markdown("(2025NOV, Q5.7) \n" \
                    "\n Consider the following from TEXT 5C."
                    "\n" \
                    "\n Comment on whether the visualisation of the statistic is effective. (2)")

    with st.container(border=True):
        st.subheader("Pure Understanding (PU):")
        st.metric(label= "Average % of marks in P1:", value= qtype_avg['Pure Understanding'], format='percent')
        st.text("These are also the most difficult questions as they typically demand that you engage directly with meaning and " \
        "show that you understand ideas in your own words. The key skills are vocabulary and ability to infer meaning. " \
        "These types of questions can also focus on argumentation and picking up on a writer's logic. ")

        expand = st.expander("Example 1")
        expand.markdown("(2024MAY, Q1.8) \n" \
        "\n" \
        "Refer to paragraph 11 and the scientists' Facebook page in paragraph 6. \n " \
        "\n " \
        "Comment on the effectiveness of social media's ability to educate people about science. (3)")

        expand = st.expander("Example 2")
        expand.markdown("(2024MAY, Q4.1.1) \n" \
                    "\n Refer to line 2: 'It's a word with old parents.'" \
                    "\n" \
                    "\n Explain how the respect that the speaker feels toward the word 'armamentarium' is expressed. (2)")

    with st.container(border=True):
        st.subheader("Language Focused (LF):")
        st.metric(label= "Average % of marks in P1:", value= qtype_avg['Language Focused'], format='percent')
        st.text("These are pure language and grammar skill questions. The mechanics, the nuts and bolts of English include: " \
        "parts of speech, syntax, sentence structure, punctuation. They can connect to style but the core is " \
        "language knowledge. Some of them can be very niche and require specific word knowledge (eg. apart vs a part). " \
        "The majority are in fact extremely predictable (e.g: active vs passive, initialism vs acronym, your vs you're). " )

        expand = st.expander("Example 1")
        expand.markdown("(2025NOV, Q1.4) \n" \
        "\n" \
        "Refer to paragraph 3.\n " \
        "\n " \
        "Explain why the writer has used rhetorical questions in this paragraph. (3)" )

        expand = st.expander("Example 2")
        expand.markdown("(2025NOV, Q6.3) \n" \
                    "\n Refer to lines 6-8 below:" \
                    "\n" \
                    "\n Explain whether 'recovered and regained' is an example of tautology. (1)")
    
    with st.container(border=True):
                        st.subheader("Comparative (C):")
                        st.metric(label= "Average % of marks in P1:", value= qtype_avg['Comparative'], format='percent')
                        st.text("Usually placed at the end of sections these questions are perceived to be the most challenging. " \
                        "Your are required to compare one text/image/poem to one or more other sources. They usually have high mark allocations. " \
                        " These questions are actually easier than believed to be. They are quite open ended, and the answering technique" \
                        " is broadly similar for this specific question type. It may be difficult to get full marks, " \
                        "but it is often very easy to get 2.5/4 or 3/5. They are often prefaced by use of the word 'critically'. " )

                        expand = st.expander("Example 1")
                        expand.markdown("(2025NOV, Q3.5) [Probably the most difficult one I have seen!] \n" \
                        "\n" \
                        "Refer to 'Remember' (TEXT 3A), 'Ozymandias of Egypt' (TEXT 3B), and the extract below, and answer the question that follows. \n " \
                        "\n " \
                        "**Critically evaluate** whether each poet makes effective use of the sonnet form to explore 'inner conflict and self-awareness' and " \
                        "ultimately 'resolves emotional struggles'. Refer to specific details from TEXT 3A and TEXT 3B to support your response. (5)")
                
                        expand = st.expander("Example 2")
                        expand.markdown("(2025NOV, Q1.8) [Seen Poetry comparative questions are often used in the comp sections as well.] \n" \
                                    "\n Refer to TEXT 1 and the seen poem, 'nobody loses all the time', by ee cummings below, and then answer the question that follows." \
                                    "\n" \
                                    "\n Critically discuss how the writer of TEXT 1 (Emily O'Neil) might respond to the speaker's view of Uncle Sol " \
                                    "in 'nobody loses all the time'. Refer to specific diction from TEXT 1, and the poem 'nobody loses all the time' " \
                                    "to support your answer. (4)")

    with st.container(border=True):
                        st.subheader("Summary")
                        st.metric(label= " % of marks in P1 ALWAYS:", value= qtype_avg['Summary'], format='percent')
                        st.text("Highly predictable question type and skill. Audience and context shifts in the question must be read carefully. " \
                        "Make sure to always draw at least one point from the shorter sources. Answering strategy/method is highly replicable here. " \
                        "Fairly easy marks if prepared. ")
    
                           