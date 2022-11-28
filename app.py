import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pycaret as pyc
import neattext.functions as ntt
import seaborn as sns
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

global_col_list = ['course_id','course_title','url','is_paid','price','num_subscribers','num_reviews','num_lectures','level','content_duration','published_timestamp','subject']
rep_data = pd.DataFrame(columns=global_col_list)
global global_data
global_data = pd.DataFrame(columns=global_col_list)
global user_text
user_text = ""
test = []

if 'global' not in st.session_state:
    st.session_state['global'] = global_data = pd.DataFrame(columns=global_col_list)
if 'rep_data' not in st.session_state:
    st.session_state['rep_data'] = rep_data = pd.DataFrame(columns=global_col_list)

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = user_text = ""


def load_data_from_source():
    data_read = pd.read_csv('udemy_courses.csv')
    datadf = pd.DataFrame(data_read)
    return datadf

def initialize_pandasDf():
    input_df = load_data_from_source()
    return input_df

def page1():
    st.header("Course Recommendation")

    def user_input():
        disable = True
        text_input = st.text_input("Enter a course name", "")

        cost_input = st.selectbox('Cost', list(("Pay", "Free", "Both")))
        if cost_input == "Pay" or cost_input == "Both":
            disable = False

        max_input = st.slider("Pick your cost range",
                    min_value=0.0, max_value=250.00, step=10.00, disabled=disable)

        # subject_input = st.multiselect('Subjects', [
        #     'Business Finance', 'Graphic Design', 'Musical Instruments', 'Web Development'])

        # level_input = st.multiselect(
        #     'Level', ['All Levels', 'Expert', 'Intermediate', 'Beginner'])

        if text_input != "" :
            return dict(user_input_text=text_input, cost=cost_input,
                        max_range=max_input)

    def implementBM25(inDataFrame):
        inDataFrame['course_title_cleaned'] = inDataFrame['course_title'].apply(ntt.remove_stopwords)
        inDataFrame['course_title_cleaned'] = inDataFrame['course_title_cleaned'].apply(ntt.remove_special_characters)
        inDataFrame['course_title_cleaned'] = inDataFrame['course_title_cleaned'].str.lower()
        actualCorpus = inDataFrame['course_title_cleaned'].to_list()
        tokenizedCorpCont = [content.split(" ") for content in actualCorpus]
        bm25matrix = BM25Okapi(tokenizedCorpCont)
        return bm25matrix, actualCorpus

    def recommend_courses(userText, inDataFrame,f_actualCorpus, f_bm25matrix):
        userText = userText.lower()
        tokenized_text = userText.split(" ")
        return_list = f_bm25matrix.get_top_n(tokenized_text, f_actualCorpus, n = 100)
        course_ind = pd.Series(inDataFrame.index, index=inDataFrame['course_title_cleaned'])
        df_col_list = ['course_id','course_title','url','is_paid','price','num_subscribers','num_reviews','num_lectures','level','content_duration','published_timestamp','subject']
        proc_df = pd.DataFrame(columns=df_col_list)
        crse_idx = [course_ind[item] for item in return_list]
        for idx in crse_idx:
            proc_df = proc_df.append(inDataFrame.loc[idx],ignore_index=True)
        return proc_df

    def additionalContentFiltering(cost_Ip, max_Ip, bmRes):
        bmRes = bmRes.drop(bmRes[bmRes.price > max_Ip].index)
        if(cost_Ip == 'Free'):
            bmRes = bmRes.drop(bmRes[bmRes.is_paid == 'TRUE'].index)
        elif(cost_Ip == 'Pay'):
            bmRes = bmRes.drop(bmRes[bmRes.is_paid == 'FALSE'].index)
        return bmRes

    def display_output(rlist):
        st.dataframe(data=rlist.loc[:,rlist.columns != 'course_title_cleaned'])

    user_info = user_input()
    
    if user_info:
        ingress_df = initialize_pandasDf()
        (bm25M, corp) = implementBM25(ingress_df)
        recommended_raw_course_listing = recommend_courses(user_info['user_input_text'], ingress_df, corp, bm25M)
        recom_list = additionalContentFiltering(user_info['cost'], user_info['max_range'],recommended_raw_course_listing)
        
        rep_data = recom_list.copy(deep=True)
        st.session_state['rep_data'] = st.session_state['rep_data'].append(rep_data)

        user_text = user_info['user_input_text']
        #st.session_state['user_input'] = st.session_state['user_input'] + " " + user_text

        display_output(recom_list)

def page2():
    st.header('Data Visualization')

    def sortedCourses(subject, base):
        courses = []

        for index, row in df.iterrows():
            if row['subject'] == subject:
                courses.append(row)

        newDf = pd.DataFrame(
            courses, columns=['course_title', 'url', 'price', base, 'content_duration'])

        sortedDf = newDf.sort_values(
            by=[base], ascending=False)
        return sortedDf

    df = initialize_pandasDf()
    question = st.radio(
        'Choose a question?',
        (
            'Average cost of course for each subject',
            'Top 5 courses for each subject based on subscribers',
            'Highest number of reviews per subject',
            'Distribution of free and paid courses for each subject'
        )
    )

    if question == 'Average cost of course for each subject':
        fig = plt.figure(figsize=(12, 10))
        plt.title("Average Cost")
        bp = sns.barplot(
            data=df, x="subject", y="price",
            width=0.5,
            errorbar=None
        )
        bp.bar_label(bp.containers[0])
        st.pyplot(fig)

    if question == 'Top 5 courses for each subject based on subscribers':
        option = st.selectbox("Choose a Subject", ('Business Finance',
                              'Musical Instruments', 'Web Development', 'Graphic Design'))

        top_5 = sortedCourses(option, 'num_subscribers').head(5)

        st.table(top_5)

    if question == 'Highest number of reviews per subject':
        option = st.selectbox("Choose a Subject", ('Business Finance',
                              'Musical Instruments', 'Web Development', 'Graphic Design'))

        highestReviews = sortedCourses(option, 'num_reviews').head(10)

        st.table(highestReviews)

    if question == 'Distribution of free and paid courses for each subject':
        fig = plt.figure(figsize=(12, 10))
        plt.title("Free courses vs Paid course")
        cp = sns.countplot(
            data=df, x="subject",
            width=0.5,
            hue="is_paid",
        )

        cp.bar_label(cp.containers[0])
        cp.bar_label(cp.containers[1])
        st.pyplot(fig)

def page3():
    st.header('Static User Dashboard')

    x=st.write(st.session_state['rep_data'])
    y=st.write(st.session_state['user_input'])

    def savedRecoms(f_rep_data, f_user_text):
        #f_rep_data['keyword_used_in_search'] = f_user_text
        global global_data
        global_data = st.session_state['global'] = st.session_state['global'].append(f_rep_data)

    
    savedRecoms(x, y)

page_names = {
    "Main": page1,
    "Data Info": page2,
    "Static Dashboard": page3
}

page_selected = st.sidebar.selectbox("Select page", page_names.keys())
page_names[page_selected]()
