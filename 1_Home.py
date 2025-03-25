import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from dataclasses import dataclass
from typing import Literal
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gemini import generate
import base64
from conversation_formatter import make_csv
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from PIL import Image
import models
import pandas as pd
import sqlite3
from rapidfuzz import process, fuzz

from st_models import Person

LOGO = "static/emory_hack_logo.png"

st.set_page_config(
    page_title="ReferAI", 
    layout="wide",
    )



with open("static/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st.logo(LOGO, icon_image=LOGO, size="large")
st.title("ReferAI")

# Title
st.markdown("<h2><strong>The Right Doctor. The Right Time.</strong></h2>", unsafe_allow_html=True)


# chat section

@dataclass
class Message:
    origin: Literal["human", 'ai']
    message: str

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "num_responses" not in st.session_state:
        st.session_state.num_responses = 0
    if "specialty" not in st.session_state:
        st.session_state.specialty = ""
    if "search_results" not in st.session_state:
        st.session_state.search_results = None
    if "current_user" not in st.session_state:
        st.session_state.current_user = Person("", "", "", "", "", "", "")
    
def on_click_callback():
    human_prompt = st.session_state.human_prompt
    llm_response = generate(human_prompt, st.session_state.history, st.session_state.num_responses)
    current_response = llm_response[0]
    report_info = llm_response[1]
    specialty = llm_response[2]
    st.session_state.num_responses += 1
    st.session_state.history.append(Message("human", human_prompt))
    st.session_state.history.append(Message("ai", current_response))
    st.session_state.human_prompt = ""
    st.session_state.specialty = specialty
    if len(report_info) > 0:
        make_csv(report_info, upload = False)
        print(specialty)
        #models.search_doctors(specialty)

def on_restart_callback():
    st.session_state.history = []
    st.session_state.num_responses = 0
    st.session_state.specialty = ""
    st.session_state.search_results = None
    st.rerun()


initialize_session_state()

chat_container = st.container(key="chat-container")
prompt_container = st.form("chat-form")
credit_card_placeholder = st.empty()

with chat_container:
    for message in st.session_state.history:
        img_path = (
        "static/person_icon_emory_hacks.png"
        if message.origin == "human"
        else
        "static/robot_icon_emory_hacks.png"
        )    
        rev = '' if message.origin == "ai" else 'row-reverse'
        ai_human_bubble = (   
            'ai-bubble' 
            if message.origin == 'ai' 
            else 
            'human-bubble'
        )
        div = f"""
            <div class="chat-row {rev}">
            <img src="data:image/png;base64,{base64.b64encode(open(img_path, 'rb').read()).decode()}" width="32" height="32">
                <div class="chat-bubble {ai_human_bubble}">{message.message}</div>
            </div>
        """
        st.markdown(div, unsafe_allow_html= True)

with prompt_container:
    st.markdown("**ReferAI Medical Assistant** - _press Enter to send a message_")
    cols = st.columns((6, 1))
    cols[0].text_input(
        "Chat",
        placeholder='Symptoms, conditions, help...',
        label_visibility='collapsed',
        key='human_prompt'
    )
    cols[1].form_submit_button(
        "",
        icon=":material/send:",
        type="primary",
        on_click=on_click_callback
    )

if st.button("Restart Chat"):
    on_restart_callback()
if st.session_state.specialty != "":
    with open("conversation.pdf", "rb") as pdf_file:
        st.download_button("Download Conversation", file_name="conversation.pdf", data=pdf_file, mime="application/pdf")
    

data_placeholder = st.empty()

def search_button_callback():
    if st.session_state.specialty == "":
        st.error("Please finish a chat with the chatbot before searching.")
        return
    # Perform the search and store the results in session state
    path = "doctors_georgia.csv"
    specialty = st.session_state.specialty.upper().strip()
    city = st.session_state.current_user.location
    df = pd.read_csv(path)
    #find ratio of matches of specialty column values to st.session_state.specialty, then filter df
    matches = df["Specialty"].apply(lambda x: process.extractOne(specialty, [x], scorer=fuzz.ratio))
    df["Match_Score"] = matches.apply(lambda x: x[1] if x else 0)
    s_fil_df = df[df["Match_Score"] > 90]

    c_fil_df = s_fil_df[s_fil_df["City"].str.contains(city, case=False)]
    best_doc = c_fil_df.sort_values(by="Rating", ascending=False)
    if best_doc.empty:
        st.error("No doctors found. Sorry!")
        return
    # Store the results in session state
    st.session_state.search_results = best_doc
    print(best_doc)

# Search section
search_cols = st.columns((6, 1))
search_cols[0].markdown('<h2>Find the right doctor for you!</h2>', unsafe_allow_html=True)
if (st.session_state.current_user.location != "" and st.session_state.specialty != ""):
    search_cols[1].button("Search", on_click=search_button_callback)

# Display the results if they exist
if st.session_state.search_results is not None:
    with data_placeholder:
        st.write(st.session_state.search_results)
set_location_text_placeholder = st.empty()

st.markdown("Set your location in Profile Information and complete a chat in order to search for doctors.")
if st.button("Go to Profile Information"):
    switch_page("Profile_Information")

# Footer
