from dataclasses import dataclass

import streamlit as st


@dataclass
class Person:
    email: str
    password: str
    fn: str
    ln: str
    dob: str
    sex: str
    location: str


def load_css():
    with open("static/style.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
