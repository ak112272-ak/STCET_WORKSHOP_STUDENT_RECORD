import streamlit as st
import sqlite3
import pandas as pd

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    department TEXT,
    semester INTEGER,
    email TEXT,
    phone TEXT
)
""")
conn.commit()


# -----------------------------
# Functions
# -----------------------------

def add_student(name, age, gender, department, semester, email, phone):
    cursor.execute("""
    INSERT INTO students(name,age,gender,department,semester,email,phone)
    VALUES(?,?,?,?,?,?,?)
    """,(name,age,gender,department,semester,email,phone))
    conn.commit()


def view_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    return rows


def delete_student(student_id):
    cursor.execute("DELETE FROM students WHERE id=?",(student_id,))
    conn.commit()


def update_student(student_id,name,age,gender,department,semester,email,phone):
    cursor.execute("""
    UPDATE students
    SET
    name=?,
    age=?,
    gender=?,
    department=?,
    semester=?,
    email=?,
    phone=?
    WHERE id=?
    """,(name,age,gender,department,semester,email,phone,student_id))
    conn.commit()


def search_student(keyword):
    cursor.execute("""
    SELECT * FROM students
    WHERE
    name LIKE ?
    OR department LIKE ?
    """,('%'+keyword+'%','%'+keyword+'%'))
    return cursor.fetchall()


# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(
    page_title="Student Record Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Record Management System")

menu = [
    "Home",
    "Add Student",
    "View Students",
    "Update Student",
    "Delete Student",
    "Search Student"
]

choice = st.sidebar.selectbox("Menu",menu)

# -----------------------------------
# Home
# -----------------------------------

if choice=="Home":

    st.header("Dashboard")

    data=view_students()

    st.metric("Total Students",len(data))

    if len(data)>0:
        df=pd.DataFrame(data,columns=[
            "ID","Name","Age","Gender","Department",
            "Semester","Email","Phone"
        ])

        st.dataframe(df,use_container_width=True)


# -----------------------------------
# Add Student
# -----------------------------------

elif choice=="Add Student":

    st.header("Add Student")

    with st.form("student_form"):

        name=st.text_input("Student Name")

        age=st.number_input("Age",18,50)

        gender=st.selectbox("Gender",
                            ["Male","Female","Other"])

        department=st.selectbox(
            "Department",
            [
                "Computer Science",
                "Information Technology",
                "Electronics",
                "Mechanical",
                "Civil",
                "Business"
            ])

        semester=st.number_input(
            "Semester",
            1,
            8
        )

        email=st.text_input("Email")

        phone=st.text_input("Phone")

        submit=st.form_submit_button("Add Student")

        if submit:

            add_student(
                name,
                age,
                gender,
                department,
                semester,
                email,
                phone
            )

            st.success("Student Added Successfully")


# -----------------------------------
# View Students
# -----------------------------------

elif choice=="View Students":

    st.header("Student Records")

    data=view_students()

    df=pd.DataFrame(data,columns=[
        "ID","Name","Age","Gender",
        "Department","Semester",
        "Email","Phone"
    ])

    st.dataframe(df,use_container_width=True)

    csv=df.to_csv(index=False).encode()

    st.download_button(
        "Download CSV",
        csv,
        "students.csv",
        "text/csv"
    )


# -----------------------------------
# Update Student
# -----------------------------------

elif choice=="Update Student":

    st.header("Update Student")

    data=view_students()

    ids=[i[0] for i in data]

    if ids:

        selected=st.selectbox(
            "Select Student ID",
            ids
        )

        record=None

        for i in data:
            if i[0]==selected:
                record=i

        if record:

            with st.form("update_form"):

                name=st.text_input("Name",record[1])

                age=st.number_input(
                    "Age",
                    18,
                    50,
                    value=record[2]
                )

                gender=st.selectbox(
                    "Gender",
                    ["Male","Female","Other"],
                    index=["Male","Female","Other"].index(record[3])
                )

                department=st.text_input(
                    "Department",
                    record[4]
                )

                semester=st.number_input(
                    "Semester",
                    1,
                    8,
                    value=record[5]
                )

                email=st.text_input(
                    "Email",
                    record[6]
                )

                phone=st.text_input(
                    "Phone",
                    record[7]
                )

                submit=st.form_submit_button(
                    "Update Student"
                )

                if submit:

                    update_student(
                        selected,
                        name,
                        age,
                        gender,
                        department,
                        semester,
                        email,
                        phone
                    )

                    st.success("Updated Successfully")

    else:
        st.warning("No records found.")


# -----------------------------------
# Delete Student
# -----------------------------------

elif choice=="Delete Student":

    st.header("Delete Student")

    data=view_students()

    ids=[i[0] for i in data]

    if ids:

        selected=st.selectbox(
            "Student ID",
            ids
        )

        if st.button("Delete"):

            delete_student(selected)

            st.success("Deleted Successfully")

    else:

        st.warning("No students available.")


# -----------------------------------
# Search Student
# -----------------------------------

elif choice=="Search Student":

    st.header("Search Student")

    keyword=st.text_input(
        "Enter Name or Department"
    )

    if st.button("Search"):

        result=search_student(keyword)

        if result:

            df=pd.DataFrame(result,columns=[
                "ID","Name","Age","Gender",
                "Department","Semester",
                "Email","Phone"
            ])

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.warning("No student found.")
