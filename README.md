<h1>Reflection Tool Application: English IEB Paper 1</h1>


 <div align="center">
  <img src="Data/Gemini_Generated_Image_n2vtz3n2vtz3n2vt.png" height="60%" width="60%"><br>
  <b>Maven Music</b>
</div>

<br />
<h2>Project Description</h2>
<p>
This project combined two worlds of my experience: English Teaching and Data Analytics. Paper 1 is a source of frustration for many students and teachers. Usually, it takes years of 
teaching experience to gain an intuition for the most obvious question types to target and the best methods to use. In this project, a complete analysis of a number of final papers 
is given, where I developed my own framework to focus on questions types and concepts rather than section by section analysis because there is actually a huge degree of overlap in skills 
between sections. 

This project also allowed me to implement much of what I have learned from creating the data, cleaning it exploring it, and finally deploying it in the form of a Streamlit app. 
The insights derived from the EDA, are displayed in a dashboard format, which allows students and teachers to track the most frequently occurring concepts that crop up in various
question types. 

The most dynamic part of the application allows users to submit their results for past papers and receive a report detailing what question types they can most improve in, and what 
concepts most urgently require revision. 
</p>
</p>

<h2>Languages and Utilities Used</h2>

- <b>Excel</b>
- <b>Python</b>
- <b>Focus on: pandas, numpy, seaborn, matplotlib, plotly</b>
- <b>Git & GitHub – Source control, version history management, and portfolio deployment.</b>
- <b>Command line prompting</b>
- <b>HTML </b>
- <b>Streamlit - for app design and deployment </b>

<h2> Skills </h2>

- <b>Data prep and EDA workflow.</b>
- <b>Approaching the scope for a project.</b> 
- <b>Gathering Data, Cleaning Data: data types, missing data, imputing data, handling text and typos, duplicates, outliers.</b>
- <b>EDA: filtering, sorting, grouping, joining, visualisation.</b>
- <b>App development and data management; designed to update all metrics and tools as more data is potentially added over time.</b>
- <b></b> 


</br>

<h2>Reflection and Questions</h2>


<b>1. Maven Music Project (and EDA course more generally)</b>

The aim of the project was to investigate the increasing churn rate a 'Maven Music Store', for which the data were complied synthetically. The course as. a whole and the mini-project went quickly for me. From my statistics courses, the understanding of outliers, distributions, scaling and transformation of variables etc. was already in place. From the previous SQL project and dashboard, I was also familiar with the processes of filtering, sorting, joining.

 What I gained was primarily, adapting these process to a python workflow with the view of using python for the machine learning application in the future. The python workflow is catching. Already after this project I can see how convenient it is to structure an investigation in one primary environment. Pandas has so much flexibility! In particular the Date Time processing, the creation of dummy variables, tha handy methods for dealing with NaN values and duplicates stood out for me has extremely well thought out. It would not take long for all these tools to become second nature.

 Because of my familiarity with base python, I learnt a few lessons in workflow. I was in the habit of saving process as multiple variables, but they quickly pile up. I learnt quickly not to update the original data frame and to use the data manipulations with some consideration and testing before saving the change or manipulation to a new variable as table. I can also make better use of the chaining capabilities of methods and attributes to be more efficient. I enjoyed using Jupyter as a tool for validation and exploration. Going back to a <b>.dtypes</b> or <b>.values_counts()</b> output after a change was made became a handy way of confirming changes to category allocations or data types. 

 The flexibility of python as a tool is incredible. Not only does it record your methods and thinking, but it also serves as a reproducible process that could easily be applied to data inputs in the same form. I see the advantage of working with smaller chunks of data, say a month or three, before leaping to apply the analysis over years. The reproducibility helps to build up the analysis form stage to stage. 

 Moreover, after the cleaning, the EDA allows you to decompose the data into multiple mini tables creating new combinations of insights. For example, when determining the user percentage of listening to Pop and Podcasts, joins and counts  and groupbys between multiple tables allowed me to arrive at the solution and then simply combine the percentage found to the final model table. Data is easily broken down, put into new combinations, and metrics, and then recombined into final tables -- this is the essential process of investigation and model development and EDA is critical. Also, in place of using the <b>.count()</b> and <b>.len()</b> methods I applied ot achieve this the solution simply used a <b>.getdummies()</b> approach to achieve the same outcome. There a multiple ways of achieving the same outcome.  

 The final product was a model table geared towards prediction using a logistic model approach to determine if a customer would cancel or not. It was already found in the exploration that the customers who were given discounts that would then expire would be a high coefficient feature for modeling the outcome.  

<p align='center'>
<img src="Data/discount.png" height="50%" width="50%"/>
</p>

</br>

<b>2. Key reflections and insights:</b>

</br>


-  <b>The plotting, especially using the handy seaborn .pairplot() function, is powerful</b>
-  <b> When there is lots of discrete and binomial data correlation metrics can be more useful. </b>
-  <b>I know in R there is method used to overcome overlapping point using a "jitter", I need to investigate the Python equivalent. </b>
-  <b>My modeling in R is sound, but I cannot wait to combine this EDA process with modeling in Python.</b>
- <b> The course gave important insight into the Scoping process; in the end this is where project experience and interaction with stakeholders matters most. </b>
- <b> Terminology is surprisingly slippery. I often panic that I do not know what a 'label' or 'feature' is, but it is such a relief to find these terms are just standard substitutes for "Response" and "Explanatory" variables etc.  </b> 
- <b> I really value the outline to "Supervised" and "Unsupervised Learning". I am already familiar with much of the modeling and classification techniques used here! I just need to update my Python processes. 


  

<!--
 ```diff
- text in red
+ text in green
