import sqlite3
from dataclasses import dataclass

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from helper_methods import Person, load_css

LOGO = "static/emory_hack_logo.png"

st.set_page_config(page_title="Log in", layout="wide", page_icon=LOGO)

load_css()

st.logo(LOGO, icon_image=LOGO, size="large")


def initialize_session_state():
    if "current_user" not in st.session_state:
        st.session_state.current_user = Person("", "", "", "", "", "", "")
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False


initialize_session_state()

if st.session_state.logged_in:
    st.success(f"You're already logged in as {st.session_state.current_user.email}")
    if st.button("Go to Home"):
        switch_page("Home")
    st.stop()


def check_login(email, password):
    conn = sqlite3.connect("emory_hack.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    data = c.fetchall()
    conn.close()
    if len(data) == 0:
        return False
    return True


login, signup = st.tabs(["**Login**", "**Sign Up**"])

with login:
    with st.form("login-form", clear_on_submit=True, border=True) as login_form:
        email = st.text_input("Email", key="email-text", placeholder="Enter email")
        password = st.text_input(
            "Password", key="password-text", placeholder="Enter password"
        )
        submitted = st.form_submit_button("**Log in**", type="secondary")
        if submitted and check_login(email, password):
            conn = sqlite3.connect("emory_hack.db")
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = c.fetchone()
            conn.close()
            if user:
                st.session_state.current_user = Person(
                    email=user[0],
                    password=user[1],
                    fn=user[2],
                    ln=user[3],
                    dob=user[4],
                    sex=user[5],
                    location=user[6],
                )
                st.session_state.logged_in = True
                st.session_state.chatbot_error_message = ""
                st.success("Login successful!")
                st.switch_page("pages/Home.py")
        elif submitted:
            st.error("Invalid email or password")
with signup:
    with st.form("signup-form", clear_on_submit=True, border=True) as login_form:
        email = st.text_input("Email", key="email-text2", placeholder="Email")
        password = st.text_input(
            "Password", key="password-text2", placeholder="Password"
        )
        verify_password = st.text_input(
            "Verify Password",
            key="verify-password-text",
            placeholder="Type your password again",
        )
        submitted = st.form_submit_button("**Sign up**", type="secondary")
        if submitted:
            conn = sqlite3.connect("emory_hack.db")
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email = ?", (email,))
            existing_user = c.fetchone()
            if email == "" or email == " ":
                st.error("Email cannot be empty")
                bottom = "Email cannot be empty"
            elif existing_user:
                st.error("User already exists")
                bottom = "User already exists"
            else:
                # signup logic here
                st.session_state.current_user.email = email
                st.session_state.current_user.password = password
                if password != verify_password:
                    st.error("Passwords do not match")
                    bottom = "Passwords do not match"
                else:
                    bottom = "Success"
                    st.success("Signup successful!")
                    st.session_state.in_signup_process = True
                    st.rerun()
                    st.switch_page("pages/Profile_Information.py")
bar, text, bar = st.columns(3)
st.markdown(
    f"""
	<h3>  </h3>
""",
    unsafe_allow_html=True,
)
