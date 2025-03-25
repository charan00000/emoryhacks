import streamlit as st
import datetime
from dataclasses import dataclass
import sqlite3
from streamlit_extras.switch_page_button import switch_page
from st_models import Person

LOGO = "static/emory_hack_logo.png"

with open("static/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st.logo(LOGO, icon_image=LOGO, size="large")
# Page title
st.title("Profile information")
existing_user=True
def initialize_session_state():
    if "current_user" not in st.session_state:
        existing_user=False
        st.session_state.current_user = Person("", "", "", "", "", "", "")

initialize_session_state()

def connect_to_db():
    conn = sqlite3.connect("emory_hack.db")
    return conn

def create_table(conn):
    c = conn.cursor()
    c.execute(f"DROP TABLE IF EXISTS users")
    conn.commit()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            email TEXT,
            password TEXT,
            first_name TEXT,
            last_name TEXT,
            dob TEXT,
            sex TEXT,
            city TEXT
        )
        """
    )
    conn.commit()

def insert_user(conn, user_data):
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (email, password, first_name, last_name, dob, sex, city)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_data.email, user_data.password, user_data.fn, user_data.ln, user_data.dob, user_data.sex, user_data.location))
    conn.commit()


with st.form("profile-info-form") as prof_info_form:
    fn = st.text_input("Legal First Name", placeholder=('Enter legal first name' if not existing_user else st.session_state.current_user.fn))
    ln = st.text_input("Legal Last Name", placeholder=('Enter legal last name' if not existing_user else st.session_state.current_user.ln))
    dob = st.date_input("Date of Birth", value=("today" if st.session_state.current_user.dob == "" 
                                                else datetime.datetime.strptime(st.session_state.current_user.dob, "%m/%d/%Y").date()), 
                                                format="MM/DD/YYYY", min_value=datetime.date(1900, 1, 1))
    location = st.text_input("City", placeholder=("Enter city") if not existing_user else st.session_state.current_user.location)
    
    placeholder_radio = st.empty()
    placeholder_add_input = st.empty()

    submitted = st.form_submit_button("Continue", type="primary")

with placeholder_radio:
    if existing_user:
        if st.session_state.current_user.sex == "MALE":
            default_index = 0
        elif st.session_state.current_user.sex == "FEMALE":
            default_index = 1
        else:
            default_index = 2
    
    sex = st.radio("Sex", [":blue[Male]", ":violet[Female]", "Other"], index = default_index)

with placeholder_add_input.container():
    if sex == "Other":
        sex = st.text_input("Other Sex", placeholder=("Enter other sex" if (st.session_state.current_user.sex == "MALE" 
                                                                            or st.session_state.current_user.sex == "FEMALE"
                                                                            or st.session_state.current_user.sex == "")
                                                                            else st.session_state.current_user.sex))
    
if submitted:
    email = st.session_state.current_user.email
    password = st.session_state.current_user.password
    if fn == "": fn = st.session_state.current_user.fn
    if ln == "": ln = st.session_state.current_user.ln
    if dob == "today": dob = st.session_state.current_user.d
    if location == "": location = st.session_state.current_user.location
    if sex == "": sex = st.session_state.current_user.sex
    st.session_state.current_user = Person(
        email, password, fn.upper(), ln.upper(), dob.strftime("%m/%d/%Y"), 
        sex.removeprefix(":blue[").removeprefix(":violet[").removesuffix("]").upper(), location.upper()
    )

    conn = connect_to_db()
    create_table(conn)
    # Check if the email already exists in the database
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    existing_user = c.fetchone()

    if existing_user:
        # Update the existing user's information
        c.execute('''
            UPDATE users
            SET password = ?, first_name = ?, last_name = ?, dob = ?, sex = ?, city = ?
            WHERE email = ?
        ''', (password, st.session_state.current_user.fn, st.session_state.current_user.ln, st.session_state.current_user.dob, st.session_state.current_user.sex, st.session_state.current_user.location, email))
        st.success("Profile updated successfully!")
    else:
        # Insert a new user if the email does not exist
        insert_user(conn, st.session_state.current_user)
        st.success("Profile created successfully!")

    conn.commit()
    conn.close()
    switch_page("Home")

    # st.write(st.session_state.current_user)