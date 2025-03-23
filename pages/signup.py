import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Sign up", layout="wide")

# Load custom CSS
with open("static/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# Header
st.markdown(
    """
    <div class="header">
        <div><strong>ReferAI</strong></div>
        <div>
            <a href="#">Help</a>
            <a href="#">Connect With Us</a>
            <a href="#">About</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("""<h2 style='text-align: center;'>Create your account</h2>""", unsafe_allow_html=True)

with st.form("signup_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")
    submitted = st.form_submit_button("Sign Up")

    if submitted:
        if not name or not email or not password or not confirm:
            st.error("Please fill in all fields.")
        elif password != confirm:
            st.error("Passwords do not match.")
        else:
            # You could replace this with actual DB logic
            st.success(f"Account created for {name}! Redirecting to login...")
            st.session_state["signed_up"] = True
            st.switch_page("home")

st.markdown("""
    <p style='text-align: center;'>Already have an account?
    <a href='#' onclick="window.location.href='/home'">Log in here</a>.</p>
""", unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">ReferAI - Your Health Assistant</div>', unsafe_allow_html=True)
