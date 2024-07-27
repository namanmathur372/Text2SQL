from dotenv import load_dotenv
load_dotenv()  ## load all the environment variables

import streamlit as st
import os 
import sqlite3
import google.generativeai as genai

## Configure our API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Model and provide SQL query as response
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt[0], question])
        return response.text
    except Exception as e:
        return str(e)

## Function to retrieve query from the SQL database
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return sql, rows
    except sqlite3.Error as e:
        return sql, str(e)

## Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    The SQL database has the following tables and columns:
    1. STUDENT(NAME, CLASS, BATCH, GRADE)
    2. TEACHER(NAME, CLASS, BATCH, GRADE)
    
    Here are some examples of how to convert English questions to SQL queries:
    
    Example 1:
    Question: How many entries of records are present in the STUDENT table?
    SQL: SELECT COUNT(*) FROM STUDENT;
    
    Example 2:
    Question: Tell me all the students studying in the Computer Science class.
    SQL: SELECT * FROM STUDENT WHERE CLASS = "Computer Science";
    
    Example 3:
    Question: What are the names of students in batch B4?
    SQL: SELECT NAME FROM STUDENT WHERE BATCH = "B4";
    
    Example 4:
    Question: List all students who have an A grade.
    SQL: SELECT * FROM STUDENT WHERE GRADE = "A";
    
    Example 5:
    Question: Count the number of students in each class.
    SQL: SELECT CLASS, COUNT(*) FROM STUDENT GROUP BY CLASS;
    
    Example 6:
    Question: Get the average grade of students in batch B3.
    SQL: SELECT AVG(GRADE) FROM STUDENT WHERE BATCH = "B3";
    
    Example 7:
    Question: Find students with grade B or higher.
    SQL: SELECT * FROM STUDENT WHERE GRADE >= "B";
    
    Example 8:
    Question: List students sorted by their names.
    SQL: SELECT * FROM STUDENT ORDER BY NAME;
    
    Example 9:
    Question: How many teachers are there in total?
    SQL: SELECT COUNT(*) FROM TEACHER;
    
    Example 10:
    Question: List all teachers who teach Computer Science.
    SQL: SELECT NAME FROM TEACHER WHERE CLASS = "Computer Science";
    
    Example 11:
    Question: Find teachers who teach in batch B4.
    SQL: SELECT NAME FROM TEACHER WHERE BATCH = "B4";
    
    Example 12:
    Question: List all teachers along with the classes they teach.
    SQL: SELECT NAME, CLASS FROM TEACHER;
    
    Example 13:
    Question: List students along with their respective teachers.
    SQL: SELECT STUDENT.NAME, TEACHER.NAME FROM STUDENT 
         JOIN TEACHER ON STUDENT.CLASS = TEACHER.CLASS 
         AND STUDENT.BATCH = TEACHER.BATCH;
    
    Example 14:
    Question: Find teachers teaching multiple batches.
    SQL: SELECT NAME FROM TEACHER GROUP BY NAME HAVING COUNT(DISTINCT BATCH) > 1;
    
    Make sure the SQL command does not have ''' in the beginning or end and the output should not include the word 'sql'.
    """
]

## Streamlit App
st.set_page_config(page_title="I can retrieve any SQL query")
st.header("Gemini App to retrieve SQL data")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

## if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    if "SQL" in response:
        st.error("Error in generating SQL query: " + response)
    else:
        sql_query, data = read_sql_query(response, "student.db")
        st.subheader("The SQL Query used is: ")
        st.code(sql_query)
        if isinstance(data, str):
            st.error("Error in executing SQL query: " + data)
        elif not data:
            st.warning("No results found.")
        else:
            st.subheader("The response is ")
            for row in data:
                st.write(row)
