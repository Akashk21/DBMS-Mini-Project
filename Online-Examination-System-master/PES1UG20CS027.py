import streamlit as st
import pandas as pd


# Security
import hashlib


import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

add_bg_from_local('flower.png')    



def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


# DB Management--------------------------------------------------------------------------------------------
import sqlite3
conn = sqlite3.connect('QPTABLE.db')
c = conn.cursor()


# DB  Functions--------------------------------------------------------------------------------------------


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS qptable(teacher TEXT,subject TEXT,questions TEXT,date DATE)')


def add_data(teacher, subject, questions, date):
    c.execute('INSERT INTO qptable(teacher,subject,questions,date) VALUES (?,?,?,?)', (teacher, subject, questions, date))
    conn.commit()


def view_all_qp():
    c.execute('SELECT * FROM qptable')
    data = c.fetchall()
    return data


def view_all_teacher():
    c.execute('SELECT DISTINCT teacher FROM qptable')
    data = c.fetchall()
    return data


def view_all_subject_of_teacher(teacher):
    c.execute('SELECT DISTINCT subject FROM qptable WHERE teacher="{}"'.format(teacher))
    data = c.fetchall()
    return data


def get_blog_by_teacher(teacher):
    c.execute('SELECT * FROM qptable WHERE teacher="{}"'.format(teacher))
    data = c.fetchall()
    return data


def get_blog_by_subject(subject):
    c.execute('SELECT * FROM qptable WHERE subject="{}"'.format(subject))
    data = c.fetchall()
    return data


def delete_data_teacher(teacher):
    c.execute('DELETE FROM qptable WHERE teacher="{}"'.format(teacher))
    conn.commit()


def delete_data_subject(teacher, subject):
    c.execute('DELETE FROM qptable WHERE teacher="{}" AND subject="{}"'.format(teacher, subject))
    conn.commit()


def querybox(query):
    c.execute(query)
    conn.commit() 

    return c.fetchall()   

# Layout--------------------------------------------------------------------------------------------
home_temp = """
<div style="background-color:#FC6444;padding:10px;border-radius:10px;margin:10px;">
<h4 style="color:#000000;text-align:center;">{}</h1>
<h6 style="color:#000000;text-align:center;">{}</h6>
<br/>
<h3 style="text-align:center">{}</h3>
</div>
"""
html_temp = """
<div style="background-color:{};padding:10px;border-radius:10px">
<h1 style="color:{};text-align:center;">Simple Blog </h1>
</div>
"""
title_temp = """
<div style="background-color:#FC6444;padding:10px;border-radius:10px;margin:10px;">
<h4 style="color:#000000;text-align:center;">Teacher:{}</h1>
<h6>Subject:{}</h6>
<br/>
<br/>
<p style="text-align:justify">{}</p>
</div>
"""
article_temp = """
<div style="background-color:#FC6444;padding:10px;border-radius:5px;margin:10px;">
<h4 style="color:#000000;text-align:center;">{}</h1>
<h6>Author:{}</h6>
<h6>Post Date: {}</h6>
<br/>
<br/>
<p style="text-align:justify">{}</p>
</div>
"""
head_message_temp = """
<div style="background-color:#FC6444;padding:10px;border-radius:5px;margin:10px;">
<h4 style="color:#000000;text-align:center;">{}</h1>
<h6>Author:{}</h6>
<h6>Post Date: {}</h6>
</div>
"""
full_message_temp = """
<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
<p style="text-align:justify;color:black;padding:10px">{}</p>
</div>
"""

#--------------------------------------------------------------------------------------------

def main():


    st.title("Online Exam Management System")

    menu = ["Home", "Login", "SignUp","querybox"]
    choice = st.sidebar.selectbox("Menu", menu)
    heading = "PES UNIVERSITY"
    subpart = "A Project By"
    names = "Akash Kumar"
    msg = """This was done under the guidance of <b>Prof. Sujthata</b>.</br>
             This is a DBMS Mini Project Class Batch 2024.</br>
             It is developed by the abovesigned.</br> Contact <a href="https://www.linkedin.com/in/akash-kumar-59382a202/">here</a>"""


    if choice == "querybox":
        st.subheader("querybox")
        query = st.text_area("Enter Your Query Here !")
        if st.button("Submit"):
            result = querybox(query)
            st.dataframe(result)
            st.stop()



    if choice == "Home":
        st.subheader("Home")
        st.markdown(home_temp.format(heading, subpart, names), unsafe_allow_html=True)
        st.markdown(full_message_temp.format(msg), unsafe_allow_html=True)

    elif choice == "Login":
        st.subheader("Login Section")
        st.info("Please log in using the side bar to continue")
        st.markdown(home_temp.format(heading, subpart, names), unsafe_allow_html=True)
        st.markdown(full_message_temp.format(msg), unsafe_allow_html=True)

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:

                st.success("Logged In as {}. Please Select the sidepane and options".format(username))

                menu1 = ["Add Question Papers", "View Question Papers", "Search Question Papers", "Manage Question Papers"]
                choice1 = st.sidebar.selectbox("QP Menu", menu1)

                if choice1 == "View Question Papers":
                    st.subheader("Question Papers in Database")
                    all_teachers = [i[0] for i in view_all_teacher()]
                    postlist = st.sidebar.selectbox("View Question Papers", all_teachers)
                    post_result = get_blog_by_teacher(postlist)
                    for i in post_result:
                        st.markdown(title_temp.format(i[0], i[1], i[3]), unsafe_allow_html=True)
                        st.markdown(full_message_temp.format(i[2]), unsafe_allow_html=True)

                elif choice1 == "Add Question Papers":
                    st.subheader("Add Question Papers To Database")
                    create_table()
                    st.markdown(full_message_temp.format("Teacher Name:"+username), unsafe_allow_html=True)
                    qp_subject = st.text_input("Enter Subject Code", max_chars=50)
                    qp_questions = st.text_area("Paste your question set here", height=200)
                    qp_date = st.date_input("Enter The Date")
                    if st.button("Add"):
                        add_data(username, qp_subject, qp_questions, qp_date)
                        st.success("Question Paper on {} by {} is saved on {}".format(qp_subject, username, qp_date))

                elif choice1 == "Search Question Papers":
                    st.subheader("Search Question Papers")
                    search_term = st.text_input('Enter Search Term')
                    search_choice = st.radio("Field to Search By", ("teacher", "subject"))
                    if st.button("Search"):
                        if search_choice == "teacher":
                            qp_result = get_blog_by_teacher(search_term)
                        elif search_choice == "subject":
                            qp_result = get_blog_by_subject(search_term)

                        for i in qp_result:
                            st.markdown(title_temp.format(i[0], i[1], i[3]), unsafe_allow_html=True)
                            st.markdown(full_message_temp.format(i[2]), unsafe_allow_html=True)

                elif choice1 == "Manage Question Papers":
                    st.subheader("Manage Question Papers Database")
                    result = view_all_qp()
                    clean_db = pd.DataFrame(result, columns=["Teacher", "Subject", "Questions", "Post Date"])
                    st.dataframe(clean_db)
                    st.markdown(full_message_temp.format("Teacher Name:"+username), unsafe_allow_html=True)

                    search_choice = st.selectbox("Field to Delete By", ["None", "teacher", "subject"])
                    if st.checkbox("Search"):
                    
                        if search_choice == "teacher":
                            unique_titles = [i[0] for i in view_all_teacher()]
                            delete_qp_by_teacher = st.selectbox("Unique Teachers", unique_titles)
                            new_df = clean_db
                            if st.button("Delete"):
                                delete_data_teacher(delete_qp_by_teacher)
                                st.warning("Deleted: '{}'".format(delete_qp_by_teacher))
                    elif search_choice == "subject":
                        unique_titles = [i[0] for i in view_all_subject_of_teacher(username)]
                        delete_qp_by_subject = st.selectbox("Unique Subjects", unique_titles)
                    new_df = clean_db

                    if st.button("Delete"):
                        delete_data_subject(username, delete_qp_by_subject)
                        st.warning("Deleted: '{}'".format(delete_qp_by_subject))



            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login on the sidebar and log in to continue")


if __name__ == '__main__':
    main()
