import streamlit as st
import pandas as pd
import os
import plotly.express as px


def reflection_tool(data_source):

    st.image(os.path.join(os.getcwd(), "static", "header1.png"))
    st.page_link(page="https://www.youtube.com/channel/UCCDNh1fC2C93zzyIj15fC0g", label="An @English_hacked reflective tool")

    st.title("Reflection Tool")

    st.text("The beating heart of this tool! You can't progress without effort and without making mistakes. But you can " \
    "progress much faster if you learn to how to reflect on mistakes made and target problematic areas. This is precisely what this " \
    "tool is designed to help you achieve.\n" \
    "\n" \
    "Simply enter your results for a past paper to produce a normal section summary, but also a question-type summary that will help " \
    "you to know where to improve and offer suggestions for particular concept improvements. All of your data is stored locally on " \
    "your browser -- none of your personal data is shared and only you have access to it. Download the report to keep your results and the recommendations. \n" \
    "\n" \
    "Proceed to the 'insights' tab to explore fully the underlying concepts and skills in many of the question types. Use the 'Question Search' in the sidebar to find " \
    "similar question types in other past papers for you to actively address the areas you most want to improve in most."  )

    #Working out getting user info for a selected paper

    paper = pd.read_pickle(data_source)
    paper_list = paper['ID'].unique()

    exam_choice = st.selectbox(
        "Choose your past paper:",
        paper_list, width= 300
        )
    selected_paper = paper[paper['ID'] == exam_choice]

    input_marks = []
    with st.form("exam_form"):
        
        # Header row
        h1, h2, h3 = st.columns([1, 2, 3])
        h1.write("**Question**")
        h2.write("**Mark Obtained**")
        h3.write("**Question Total**")
        st.divider()

        # Loop to create inputs
        

        for index, row in selected_paper.iterrows():
            q_num = row['Question']
            q_total = row['Question Total']

        #Setting up loop columns
            col1, col2, col3 = st.columns([1,2,3])

        #Question number
            col1.write(f"**{q_num}**")

        #User input score
            score_input = col2.number_input(
                label = f"Score for {q_num}",
                min_value= 0.0,
                max_value= float(q_total),
                step=0.5,
                value=None,
                key=f"score_{index}",
                label_visibility="collapsed"
            )
        #Question total
            col3.write(f"    /**{q_total}**")

            input_marks.append(score_input if score_input is not None else 0.0)

        
        
        submitted = st.form_submit_button("Generate Report")
        print(input_marks)

    if submitted:
        #Adding user marks to df
        selected_paper['input_marks'] = input_marks

        with st.container(border=True):
            st.subheader(f"Report on: English P1 {exam_choice}")

            st.divider()

            st.markdown("#### 1. Typical Breakdown")

        
            st.metric("Overall Paper Result:", value= round(selected_paper['input_marks'].sum(),1)/100, format='percent')

            section_table = selected_paper.groupby('Section').agg(
                                        Section_total = ('Question Total', 'sum'),
                                        Attained = ('input_marks', 'sum')
            ).reset_index()

            custom_order = [
                "Comp",
                "Summary",
                "Seen",
                "Unseen",
                "Crit",
                "Lang"
            ]
            section_table['Section'] = pd.Categorical(section_table['Section'], categories=custom_order, ordered=True )
            section_table = section_table.sort_values("Section")

            section_table['Section_percentage'] = round((section_table['Attained']/section_table['Section_total'])*100,2)

            st.dataframe(section_table, hide_index= True)




            st.divider()

            st.markdown("#### 2. Question Type Breakdown")


            #grouping to find percentages of each question type 
            question_by_type = selected_paper.groupby('Type').agg(
                Question_type_total = ('Question Total', 'sum'),
                Attained = ('input_marks', 'sum')
            )

            question_by_type['Percentage_attained'] = round((question_by_type['Attained']/question_by_type['Question_type_total'])*100, 1)

            question_by_type = question_by_type.sort_values('Percentage_attained', ascending = False).reset_index()

            type_map ={
                'Summary': 'Summary',
                'ICQ' : "Indirect Concept Questions",
                'PU': "Pure Understanding",
                'DCQ' : 'Direct Concept Questions',
                'LF': 'Language Focused',
                'C':'Comparative',
                'VL': 'Visual Literacy'
            }
            question_by_type['Type'] = question_by_type['Type'].map(type_map)
        

            st.write("The following is ranked from your strongest to weakest percentage attainment by question type:")
            st.dataframe(question_by_type, hide_index=True)

            fig = px.bar(
                question_by_type.sort_values("Percentage_attained", ascending=True),
                x="Type",
                y="Percentage_attained",
                orientation="v",
                title="Percentage Attained for Question Type",
                labels={
                    "Type": "",
                    "Percentage_attained": "Percentage Attained (%)",
                },
                text_auto=".1f",  # Displays values like 62.5% on the bars
                color="Percentage_attained",
                color_continuous_scale="RdYlGn",  # Gradient from red (low) to green (high)
            )

            # 3. Format axes & layout
            fig.update_layout(
                yaxis=dict(range=[0, 110]),
                title_x=0.5,
                title_xanchor='center',
                coloraxis_showscale=False,  # Hide the color bar legend on the side
                height=450,
            )

            st.write("\n \n")
            st.write("\n \n " \
            "Note: the information below is the percentage attained for each question type. You can " \
            "technically attain 100% for each question type. This allows you to COMPARE and determine which question type you can focus on to maximise improvement.")
            # 4. Render in Streamlit
            st.plotly_chart(fig, width='stretch')


            # Improve in language concepts
            language_insights = selected_paper[selected_paper['Type'] == 'LF']
            language_insights = language_insights.groupby('Keywords')[['Question Total', 'input_marks']].sum().reset_index()
            
            language_insights['concept_percentage'] = language_insights['input_marks']/language_insights['Question Total']

            language_insights = language_insights[language_insights['concept_percentage'] < 1]

            language_insights.sort_values("concept_percentage", ascending=True, inplace=True)
            language_insights.reset_index(drop=True, inplace=True)
            
            
            lowest_concepts = language_insights.iloc[:5, 0].to_list()
            
            concepts_text = ', '.join(lowest_concepts)

            if lowest_concepts:
                st.info(f"You may want to revise and brush up on your **language knowledge** with respect to the following concepts: **{concepts_text}**.", icon='💡')

            else:
                st.success("Excellent job! You achieved full marks across all language concepts.", icon='🌟')

            #Improve on other concepts:

            other_insights = selected_paper[selected_paper['Type'].isin(['DCQ','ICQ','VL'])]
            other_insights = other_insights.groupby('Keywords')[['Question Total', 'input_marks']].sum().reset_index()
            
            other_insights['concept_percentage'] = other_insights['input_marks']/other_insights['Question Total']

            other_insights = other_insights[other_insights['concept_percentage'] < 1]

            other_insights.sort_values("concept_percentage", ascending=True, inplace=True)
            other_insights.reset_index(drop=True, inplace=True)
            

            lowest_concepts2 = other_insights.iloc[:5, 0].to_list()
            concepts_text2 = ', '.join(lowest_concepts2)

            if lowest_concepts2:
                st.info(f"You may want to revise and brush up on **other question types** by revising the following concepts: **{concepts_text2}**.", icon='💡')

            else:
                st.success("Excellent job! You achieved full marks across all other concepts.", icon='🌟')

            lang_checklist_html = "".join([f'<li><label><input type="checkbox"> {concept}</label></li>' for concept in lowest_concepts])
            other_checklist_html = "".join([f'<li><label><input type="checkbox"> {concept}</label></li>' for concept in lowest_concepts2])



            st.markdown("#### Tips for action: \n" \
            " - Access the sidebar to find quick definitions of the question types.\n" \
            " - Full explanation of the question types, with examples, can be found in the 'Definitions' tab.\n" \
            " - Summary question should be relatively high. This is the most predictable question type.\n" \
            " - Visual Literacy, Language Focused and Concept Questions are easy to improve on with targeted study.\n" \
            " - Comparative questions are predictable in terms of technique and how to structure responses. Work on answering technique.\n" \
            " - Pure Understanding is the most difficult to improve on. Answering technique + vocab + reading + practice = improvement. \n" \
            "- Explore the 'insights' tab to find what concepts crop up most frequently in examinations."
        )
        # Generating a downloaded file
        def generate_html_report(
            exam_choice, selected_paper, section, question_by_type, fig_plotly
        ):
            selected_paper_total = (
                round(selected_paper["input_marks"].sum(), 1) / 100
            )
            

            chart_html = fig_plotly.to_html(full_html=False, include_plotlyjs="cdn")
            section_table_html = section.to_html(classes="report-table", index = False)
            qtype_table_html = question_by_type.to_html(
                classes="report-table", index=False
            )

            return f"""<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Report: English P1 {exam_choice}</title>
            <style>
                body {{ font-family: sans-serif; margin: 40px; color: #333; line-height: 1.6; }}
                h2 {{ color: #1E293B; border-bottom: 2px solid #E2E8F0; padding-bottom: 8px; }}
                h4 {{ color: #0F172A; margin-top: 24px; }}
                .metric-card {{ background: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px; border-radius: 6px; display: inline-block; }}
                .report-table {{ width: 100%; border-collapse: collapse; margin: 16px 0; }}
                .report-table th, .report-table td {{ border: 1px solid #CBD5E1; padding: 8px 12px; text-align: left; }}
                .report-table th {{ background-color: #F1F5F9; }}
                .tips-list {{ background-color: #F8FAFC; padding: 15px 15px 15px 35px; border-radius: 6px; border-left: 4px solid #3B82F6; }}
            </style>
        </head>
        <body>
            <h2>Report on: English P1 {exam_choice}</h2>
            <h4>1. Typical Breakdown</h4>
            <div class="metric-card">
                <strong>Overall Paper Result:</strong> {selected_paper_total:.1%}
            </div>
            {section_table_html}
            <hr>
            <h4>2. Question Type Breakdown</h4>
            <p>Ranked from strongest to weakest percentage attainment by question type:</p>
            {qtype_table_html}
            <div style="margin-top: 20px;">{chart_html}</div>
            <p><em>Note: You can technically attain 100% for each question type. Use this to compare performance in question type and determine
            where you can maximise improvement.</em></p>

            <h4>Tips for action:</h4>
                        <ul class="tips-list">
                            <li>Consult the 'Definitions' and 'Insights' to see what questions you should focus on to improve.</li>
                            <li>Summary question should be relatively high. This is the most predictable question type!</li>
                            <li>Visual Literacy, Language Focused and Concept Questions are easy to improve on with targeted study (see lists below!).</li>
                            <li>Comparative questions are predictable in terms of technique and how to structure responses. Work on answering technique.</li>
                            <li>Pure Understanding is the most difficult to improve upon. Answering technique + vocab + reading + practice = improvement.</li>
                        </ul>

            <h4>3. Targeted Revision Checklist:</h4>
            <p>NOTE: these only reflect concepts particular to your revision paper and your performance. To see which concepts occur most frequently across 
            many examination papers explore the 'insights' tab.</p>

            <div class="checklist-card">
            <strong>Top 5 Language Focused Concepts to revise:</strong>
            <ul class="checklist">
            {lang_checklist_html}
            </ul>
            </div>

            <div class="checklist-card">
            <strong>Top 5 Other Question Type Concepts to revise:</strong>
            <ul class="checklist">
            {other_checklist_html}
            </ul>
            </div>

            
        </body>
        </html>"""
                    
        st.divider()
        html_data = generate_html_report(
            exam_choice, selected_paper, section_table, question_by_type, fig
        )
        st.download_button(
            label="📥 Download Report as HTML",
            data=html_data,
            file_name=f"English_P1_{exam_choice}_Report.html",
            mime="text/html",
            width='stretch',
  )
    