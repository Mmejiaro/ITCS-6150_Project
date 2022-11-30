# Udemy Course Recommendation System

> A recommendation system that provides udemy courses based on user input

> Live demo [_here_](https://drive.google.com/file/d/1f8J7du_kMKnd7VyjNMZFIWNVIIQ_Yqrh/view?usp=sharing).

## Table of Contents
* [General Info](#general-information)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Contact](#contact)

## General Information
- Students spend several minutes to hours looking for courses that benefit them
- The purpose of our project is to reduce the time that it takes to locate those courses by providing a simple interface that outputs recommended courses from Udemy based on user input


## Setup
- With the files in your preferred directory open in your perferred IDE (running through Anacanda ensures that most dependenices are already downloaded)
- Ensure you have python3 (created using version installed 3.7.15)
- Streamlit (version 1.13.0) opensource framework was used
- other libraries used - neattext, rank_bm25, pycaret
- in the terminal ensure that you are in the correct directory that contains app.py
- to run project: streamlit run app.py
- will automatically open a browser page displaying the application or click on the provide links that appear in terminal


## Usage
1. Sidebar on left, can select a page, Defaulted to Main
- Main Page
    1. Enter a course name (press enter to apply)
    2. Select cost either Pay, Free, Both (selecting Free disable range picker)
    3. Pick the maximum value that the user is willing to pay
    5. The recommended courses will appear at the bottom
- Data Info Page
    1. Choose a question from the following four provided
    2. Graphical representation / table of that data will appear at bottom based on selected question
- Static Dashboard
    1. Dependent on Main Page, Stores courses in a table based on pervious searches
    2. By default dashboard is empty with no information was inputed in Main Page
    3. Can view all courses that were searched on main page during the specific session


## Project Status
Project is: _complete_


## Contact
Created by Shreyas Lokesha, Claire Ardern, Rudhra Moorthy Baskar, and Michael Mejia

