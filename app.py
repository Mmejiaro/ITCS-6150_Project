import streamlit as st
import pandas as pd
import pycaret as pyc
import neattext.functions as ntt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("Course Recommendation System")

def load_data_from_source():
    data_read = pd.read_csv('udemy_courses.csv')
    datadf = pd.DataFrame(data_read)
    return datadf

def initialize_pandasDf():
    input_df = load_data_from_source()
    return input_df

def user_input():
    disable = True
    text_input = st.text_input("Enter a course name", "")

    cost_input = st.selectbox('Cost', list(("Pay", "Free", "Both")))
    if cost_input == "Pay" or cost_input == "Both":
        disable = False

    # TODO: replace max_value with correct value
    max_input = st.slider("Pick your cost range",
                   min_value=0.0, max_value=100.00, step=0.25, disabled=disable)

    subject_input = st.multiselect('Subjects', [
        'Business Finance', 'Graphic Design', 'Musical Instruments', 'Web Development'])

    level_input = st.multiselect(
        'Level', ['All Levels', 'Expert', 'Intermediate', 'Beginner'])

    if text_input != "" and len(subject_input) != 0 and len(level_input) != 0:
        return dict(user_input_text=text_input, cost=cost_input,
                      max_range=max_input, subjects=subject_input, level=level_input)

def implement_cosine_sim(inDataFrame):
    inDataFrame['course_title_cleaned'] = inDataFrame['course_title'].apply(ntt.remove_stopwords)
    inDataFrame['course_title_cleaned'] = inDataFrame['course_title_cleaned'].apply(ntt.remove_special_characters)
    inDataFrame['course_title_cleaned'] = inDataFrame['course_title_cleaned'].str.lower()
    cvect = CountVectorizer()
    cv_mat = cvect.fit_transform(inDataFrame['course_title_cleaned'])
    cos_sim_matrix = cosine_similarity(cv_mat, cv_mat)
    return cos_sim_matrix

def recommend_courses(userText, inDataFrame, sim):
    course_ind = pd.Series(inDataFrame.index, index=inDataFrame['course_title'])
    crse_idx = course_ind[userText]
    simscores = list(enumerate(sim[crse_idx]))
    sortedscores = sorted(simscores,key=lambda x:x[1], reverse=True)
    relevantrecom = sortedscores[1:21]
    recomList = []
    for index, sc in relevantrecom:
        recomList.append(inDataFrame.loc[index,["course_title","url","level","price","num_lectures","subject"]])
    
    return recomList

def display_output(rlist):
    st.table(rlist)

user_info = user_input()
if(user_info):
    ingress_df = initialize_pandasDf()
    sim_matrix = implement_cosine_sim(ingress_df)
    recommended_course_listing = recommend_courses(user_info['user_input_text'], ingress_df, sim_matrix)
    display_output(recommended_course_listing)


# if __name__ == "__main__":
#     user_info = user_input()

#     if user_info:
#         print (user_info)
