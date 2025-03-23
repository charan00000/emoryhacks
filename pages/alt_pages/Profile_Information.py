import streamlit as st
import datetime
from dataclasses import dataclass

LOGO = "static/emory_hack_logo.png"

with open("static/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st.logo(LOGO, icon_image=LOGO, size="large")
# Page title
st.title("Additional information")

@dataclass
class Person:
    email: str
    password: str
    fn: str
    ln: str
    dob: str
    sex: str

def initialize_session_state():
    if "current_user" not in st.session_state:
        st.session_state.current_user = Person("", "", "", "", "", "") 

initialize_session_state()

with st.form("profile-info-form") as prof_info_form:
    fn = st.text_input("Legal First Name", placeholder='Enter legal full name')
    ln = st.text_input("Legal Last Name", placeholder='Enter legal last name')
    dob = st.date_input("Date of Birth", value="today", format="MM/DD/YYYY", min_value=datetime.date(1900, 1, 1))
    
    placeholder_radio = st.empty()
    placeholder_add_input = st.empty()

    submitted = st.form_submit_button("Continue", type="primary")

with placeholder_radio:
    sex = st.radio("Sex", [":blue[Male]", ":violet[Female]", "Other"])

with placeholder_add_input.container():
    if sex == "Other":
        sex = st.text_input("Other Sex", placeholder="Enter other sex") 
    
if submitted:
    email = st.session_state.current_user.email
    password = st.session_state.current_user.password
    st.session_state.current_user = Person(
        email, password, fn.upper(), ln.upper(), dob.strftime("%m/%d/%Y"), sex.removeprefix(":blue[").removeprefix(":violet[").removesuffix("]").upper()
    )
    # st.write(st.session_state.current_user)