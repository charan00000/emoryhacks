import streamlit as st
from dataclasses import dataclass

@dataclass
class Person:
	email: str
	password: str
	fn: str
	ln: str	
	dob: str
	sex: str
	location: str

def initialize_session_state():
	if "current_user" not in st.session_state:
		st.session_state.current_user = Person("", "", "", "", "", "", "")
	if "logged_in" not in st.session_state:
		st.session_state.logged_in = False