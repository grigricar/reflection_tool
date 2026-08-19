import streamlit as st
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px




def insights(data_input):
    st.image(os.path.join(os.getcwd(), "static", "header3.png"))
    st.page_link(page="https://www.youtube.com/channel/UCCDNh1fC2C93zzyIj15fC0g", label="An @English_hacked reflective tool")

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
    paper_eda = pd.read_pickle(data_input)
    paper_eda['Type'] = paper_eda['Type'].map(new_map)
    paper_id_type_sort = paper_eda.groupby(["ID", "Type"])['Question Total'].sum().reset_index()

    st.title("Insights")
    st.write("Use this section to explore the findings made across English IEB paper Is" \
    " from 2020-2025. You can use the insights to discover how papers differ and gauge how much " \
    "benefit there is to improving specific question types. \n" \
    "\n" \
    "The final insights are particularly valuable in tracking which skills and concepts appear most " \
    "frequently across papers. You can construct handy, data informed, checklists for revision to target areas you want " \
    "to improve in most (or request last minute recaps on critical concepts from teachers!). Note: At currently only 11 papers \n" \
    "this is a small sample, so make judgments and predictions with caution.")

    st.subheader("1. Overview of Question Types in Past Papers" )
    with st.container(border=True):

        st.subheader("1.1 Exploring mark allocation by question type")
        #User filter: Paper 
        all_papers = paper_id_type_sort['ID'].unique()
        all_papers = all_papers[::-1]

        user_choice = st.multiselect(label= "Select Papers:", options=all_papers, default=all_papers )
        filtered_df = paper_eda[paper_eda['ID'].isin(user_choice)].sort_values(['ID', 'Type'])

        # User filter for q type
        
        all_qtypes = paper_eda['Type'].unique()

        user_qchoice = st.multiselect(label= "Select Q-types:", options=all_qtypes, default=all_qtypes )
        filtered_df = filtered_df[filtered_df['Type'].isin(user_qchoice)]

        
        
        
        custom_colours = [
            '#8dd3c7',
            '#ffffb3', 
            '#bebada',
            '#fb8072',
            '#80b1d3',
            '#fdb462',
            '#b3de69'
        ]
        try:
            # 1. Instantiate the figure and axis explicitly
            fig, ax = plt.subplots(figsize=(12, 8))

            # 2. Plot onto the created `ax`
            sns.histplot(
                data=filtered_df,
                x="ID",
                weights="Question Total",
                hue="Type",
                multiple="stack",
                shrink=0.8,
                palette= 'Set3',
                ax=ax,  # Pass the explicit axis here
            )

            

            # 3. Add bar segment labels
            for container in ax.containers:
                ax.bar_label(
                    container,
                    fmt="%g",
                    label_type="center",
                    fontsize=11,
                    color="black",
                )

            # 4. Use `ax` methods instead of general `plt` calls where possible
            ax.set_title("Paper Total By Question Type", fontsize=14, pad=15)
            ax.set_xlabel("Paper ID", fontsize=12)
            ax.set_ylabel("Marks By Question Type", fontsize=12)
            ax.tick_params(axis="x", rotation=45)

            # 5. Move legend outside
            sns.move_legend(
                ax,
                loc="upper left",
                bbox_to_anchor=(1, 1),
                title="Question Type",
                frameon=False,
            )

            sns.despine()
            fig.tight_layout()

            # 6. Render in Streamlit
            st.pyplot(fig)

        except ValueError:
                st.error("⚠️ Make sure a paper & q-type is selected")

        st.markdown(" #### General Findings: \n " \
        "- There are no clear trends in question type over time. DO NOT TRY TO PREDICT A PAPER! \n" \
        "- Summary, Visual Literacy and Comparative Questions do not change much from paper to paper. \n" \
        "- What do fluctuate are the marks given to Pure Understanding questions VS questions based on concepts that can be studied directly. \n " \
        "- 2025MAY and 2025NOV represent two extremes of paper type. One favours high pure reading and comprehension; the other knowledge of how to apply concepts. \n" \
        "- One recommended study approach is to **make sure you have prepared/practised on two papers of opposite extremes** eg. 2025NOV & 2025MAY; 2022MAY & 2022NOV")

        st.subheader("1.2 The average marks given to each question type")

        avg_questions = paper_id_type_sort.groupby('Type')['Question Total'].mean().round(2).reset_index().sort_values('Question Total')

        with st.expander("Question Average Table"):
            st.dataframe(avg_questions.sort_values('Question Total', ascending = False), hide_index= True)

        # 1. Instantiate the figure and axis explicitly
        fig, ax = plt.subplots(figsize=(10, 6))

        # 2. Plot onto the created `ax`
        sns.barplot(
            data=avg_questions,
            x="Type",
            y="Question Total",
            hue="Type",
            palette=custom_colours,
            ax=ax,  # Pass the explicit axis here
        )

        # 3. Add bar segment labels
        for container in ax.containers:
            ax.bar_label(
                container,
                fmt="%g",
                label_type="center",
                fontsize=11,
                color="black",
            )

        # 4. Use `ax` methods instead of general `plt` calls where possible
        ax.set_title("Average Marks Allocated to Question Type (papers: 2020-2025)", fontsize=14, pad=15)
        ax.set_xlabel("Paper ID", fontsize=12)
        ax.set_ylabel("Avg Marks By Question Type", fontsize=12)
        ax.tick_params(axis="x", rotation=45)


        sns.despine()
        fig.tight_layout()

        # 6. Render in Streamlit
        st.pyplot(fig)

        st.markdown("#### General Findings: \n" \
        "- It is more useful to use these averages for question type than to try predict trends. \n" \
        "- Pure Understanding Questions account for the largest percentage of marks in a typical paper. \n" \
        "- The large chunk of Pure Understanding (the most difficult question type to actively prepare for) is one explanation for the perceived pointlessness of preparing for paper 1. \n" \
        "- Language Focused questions tend to take up approximately 20% of the paper. Well worth putting study time into. \n" \
        "- Visual Literacy based questions take up only approximately 11% of a paper -- less than half of the crit lit section. \n" \
        "- Summary and Comparative questions are a giveaway considering how predictable their form is. Practising answering technique here will lead to improvement. \n " \
        "- Recommended study approach: if pushed for time, and looking at two extremes of P1 is not an option, **reflect and practise on a single paper that approaches the averages: 2024MAY or 2021NOV.**")

    st.subheader("2. Deep Dive into Question Type Trends:")

    with st.container(border=True):
        st.subheader('2.1 Language Focused(LF):')

        
        #data input
        lf_breakdown = paper_eda[paper_eda['Type'] == "Language Focused"]
        lf_breakdown = lf_breakdown.groupby(['ID', 'Subskill'])['Question Total'].sum().reset_index()
        

        new_labels = {
            'error' :'Common Errors',
            'language':'General Language',
            'punctuation':'Punctuation',
            'sentence structure':'Sentence Structure',
            }

        lf_breakdown['Subskill'] = lf_breakdown['Subskill'].map(new_labels)
        lf_breakdown.sort_values('ID', inplace=True)

        ID_list = lf_breakdown['ID'].unique()
        

        #bar charts
        fig = px.bar(
            lf_breakdown,
            x="ID",
            y="Question Total", 
            color="Subskill",  
            barmode="stack",  
            color_discrete_sequence=px.colors.qualitative.Set2, 
            template="simple_white",  
            title="Breakdown of Language Focused (LF) Subskills:",
            text= "Question Total", 
            labels={
                "ID": "Paper ID",
                "Question Total": "Marks By Subskill",
                "Subskill_Clean": "Language Subskills:",
            
            },
            category_orders={
                "ID": ID_list
            }
        )

        # Custom layout and axis formatting
        fig.update_layout(
            width=800,
            height=560,
            title_font_size=18,
            xaxis_tickangle=-45,  
            legend=dict(
                title_text="Subskills (click to select)",
                orientation="v",
                x=1.02,
                y=1.0,
                xanchor="left",
                yanchor="top",
                font=dict(size=10),
                title_font=dict(size=11),
            ),
            bargap=0.2,
        )
        fig.update_traces(
            texttemplate='<b>%{text}</b>',
            textposition='inside'
            )
            
        
        st.plotly_chart(fig, width='stretch')

        st.subheader('2.2 Frequency of Specific Concepts within Language Subskills')

        subskill_colour = {
        'Common Errors': "#66c2a5",
        'General Language': '#fc8d62',
        'Punctuation': '#8da0cb',
        'Sentence Structure': '#e78ac3',
                    }   

        # User selection of subskills:

        selected_subskill = st.selectbox("Select a Subskill:", options=list(subskill_colour.keys()))

        # Data prep
        paper_eda['Subskill'] = paper_eda['Subskill'].map(new_labels)
        language_subskills = paper_eda[paper_eda['Subskill'] == selected_subskill]
        language_subskills = language_subskills[['ID', 'Question', 'Keywords', 'count', 'Question Total']]
        language_subskills = language_subskills.groupby('Keywords')[['count', 'Question Total']].sum().reset_index()

        language_subskills.sort_values('count', ascending=False, inplace=True)

        with st.expander("Language subskills table"):
             st.dataframe(language_subskills[['Keywords', 'count']], hide_index=True)

        # Bargraph for concept frequency:
        title_string = f"Frequency of all concepts appearing in {selected_subskill}"
        substring_colour = subskill_colour[selected_subskill]

        fig = px.bar(
        language_subskills,
        x="count",
        y="Keywords",
        title = title_string,
        subtitle= "Taken from papers spanning 2020-2025",
        color = "Keywords",
        color_discrete_sequence=[substring_colour],
        orientation= 'h',
        text='count',
        template='plotly_white',
        height=500
        )

        fig.update_layout(
        showlegend=False,
        yaxis_title = 'Concepts',
        xaxis_title = 'Frequency of Concept From 2020-2025', 
          
        )
        fig.update_yaxes(          
        showticklabels=True  
        )

        fig.update_traces(
        textposition="inside",
        textfont=dict(weight="bold", size=16),
        
        
        )

        st.plotly_chart(fig, width='stretch')

        if selected_subskill == "General Language":
            st.write("Note: 'Word Skill' covers many word explanation questions (eg. too vs to, apart vs a part, its vs it's), and some " \
            "parts of speech questions. Many are quite common. A handful will always be discussed intensely after an examination.")
        elif selected_subskill == "Punctuation":
                st.write("Note: 'rhythm' are cases where punctuation affects the beat in a line or sentence. Common in poetry questions. ")

    with st.container(border=True):

        st.subheader("2.3 Concept Frequency in Other Question Types ")

        #Data prep

        qtype_dict = {
             'Direct Concept Question': '#fb8072',
             'Indirect Concept Question': '#8dd3c7',
             'Visual Literacy': '#bebada'
        }

        selected_qtype = st.selectbox("Select a Subskill:", options=list(qtype_dict.keys()))

        qtypes_selection = paper_eda[paper_eda['Type'] == selected_qtype]
        qtypes_selection = qtypes_selection.groupby('Keywords')[['count', 'Question Total']].sum().reset_index()

        qtypes_selection.sort_values('count', ascending=False, inplace=True)

        with st.expander("Q-types concept table"):
                    st.dataframe(qtypes_selection[['Keywords', 'count']], hide_index=True)                            

        title_string2 = f"Frequency of all concepts appearing in {selected_qtype}"
        substring_colour2 = qtype_dict[selected_qtype]

        fig = px.bar(
        qtypes_selection,
        x="count",
        y="Keywords",
        title = title_string2,
        subtitle= "Taken from papers spanning 2020-2025",
        color = "Keywords",
        color_discrete_sequence=[substring_colour2],
        orientation= 'h',
        text='count',
        template='plotly_white',
        height=800
        )

        fig.update_layout(
        showlegend=False,
        yaxis_title = 'Concepts',
        xaxis_title = 'Frequency of Concept From 2020-2025', 
            
        )
        fig.update_yaxes(          
        showticklabels=True  
        )

        fig.update_traces(
        textposition="inside",
        textfont=dict(weight="bold", size=16),
        
        
        )

        st.plotly_chart(fig, width='stretch')