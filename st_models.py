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
