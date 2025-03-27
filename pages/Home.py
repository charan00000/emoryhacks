import os
import sys
from dataclasses import dataclass
from typing import Literal

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import base64
import sqlite3

import pandas as pd
from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfReader
from rapidfuzz import fuzz, process

import models
from conversation_formatter import make_csv
from gemini import generate
from helper_methods import Person, load_css

LOGO = "static/emory_hack_logo.png"

st.set_page_config(page_title="ReferAI", layout="wide", page_icon=LOGO)

load_css()

st.logo(LOGO, icon_image=LOGO, size="large")

# Title
st.title("ReferAI")
st.markdown(
    "<h2><strong>The Right Doctor. The Right Time.</strong></h2>",
    unsafe_allow_html=True,
)


# Dataclasses for each message
@dataclass
class Message:
    origin: Literal["human", "ai"]
    message: str


# initialize session state parameters
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
    if "human_prompt" not in st.session_state:
        st.session_state.human_prompt = ""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "chatbot_error_message" not in st.session_state:
        st.session_state.chatbot_error_message = ""


initialize_session_state()


# define all callback functions
# calback for each chat meassage
def on_click_callback():
    human_prompt = st.session_state.human_prompt
    llm_response = generate(
        human_prompt, st.session_state.history, st.session_state.num_responses
    )
    current_response = llm_response[0]
    report_info = llm_response[1]
    specialty = llm_response[2]
    st.session_state.num_responses += 1
    st.session_state.history.append(Message("human", human_prompt))
    st.session_state.history.append(Message("ai", current_response))
    st.session_state.human_prompt = ""
    st.session_state.specialty = specialty
    st.session_state.chatbot_error_message = ""
    if len(report_info) > 0:
        make_csv(report_info, upload=False)
        print(specialty)


# callback for restarting the chat
def on_restart_callback():
    st.session_state.history = []
    st.session_state.num_responses = 0
    st.session_state.specialty = ""
    st.session_state.search_results = None
    st.session_state.human_prompt = ""
    st.session_state.chatbot_error_message = ""


# callback for searching for doctors
def search_button_callback():
    if st.session_state.specialty == "":
        st.session_state.chatbot_error_message = (
            "Please finish a chat with the chatbot before searching."
        )
        return
    if st.session_state.current_user.location == "":
        st.session_state.chatbot_error_message = (
            "Please set your location in Profile Information before searching."
        )
        return
    # Perform the search and store the results in session state
    path = "doctors_georgia.csv"
    specialty = st.session_state.specialty.upper().strip()
    city = st.session_state.current_user.location
    df = pd.read_csv(path)
    # find ratio of matches of specialty column values to st.session_state.specialty, then filter df
    matches = df["Specialty"].apply(
        lambda x: process.extractOne(specialty, [x], scorer=fuzz.ratio)
    )
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


chat_container = st.container(key="chat-container")
prompt_container = st.form("chat-form")
credit_card_placeholder = st.empty()

with chat_container:
    for message in st.session_state.history:
        img_path = (
            "static/person_icon_emory_hacks.png"
            if message.origin == "human"
            else "static/robot_icon_emory_hacks.png"
        )
        rev = "" if message.origin == "ai" else "row-reverse"
        ai_human_bubble = "ai-bubble" if message.origin == "ai" else "human-bubble"
        div = f"""
            <div class="chat-row {rev}">
            <img src="data:image/png;base64,{base64.b64encode(open(img_path, 'rb').read()).decode()}" width="32" height="32">
                <div class="chat-bubble {ai_human_bubble}">{message.message}</div>
            </div>
        """
        st.markdown(div, unsafe_allow_html=True)

with prompt_container:
    st.markdown("**ReferAI Medical Assistant** - _press Enter to send a message_")
    cols = st.columns((6, 1))
    cols[0].text_input(
        "Chat",
        placeholder="Symptoms, conditions, help...",
        label_visibility="collapsed",
        key="human_prompt",
    )
    cols[1].form_submit_button(
        "", icon=":material/send:", type="primary", on_click=on_click_callback
    )

st.button("Restart Chat", on_click=on_restart_callback)
if st.session_state.specialty != "":
    with open("conversation.pdf", "rb") as pdf_file:
        st.download_button(
            "Download Conversation",
            file_name="conversation.pdf",
            data=pdf_file,
            mime="application/pdf",
        )


data_placeholder = st.empty()
error_placeholder = st.empty()
with error_placeholder:
    if st.session_state.chatbot_error_message != "":
        st.error(st.session_state.chatbot_error_message)

# Search section
search_cols = st.columns((6, 1))
search_cols[0].markdown(
    "<h2>Find the right doctor for you!</h2>", unsafe_allow_html=True
)
if (
    st.session_state.current_user.location is not None
    and st.session_state.specialty is not None
):
    search_cols[1].button("Search", on_click=search_button_callback)


def doctor_card(name, specialty, city, state, rating, profile_url):
    stars = "⭐" * round(rating)

    st.markdown(
        f"""
        <a href="{profile_url}" target="_blank" style="text-decoration: none; color: inherit;">
            <div style="
                background-color: #f6f8fc; 
                padding: 16px; 
                border-radius: 16px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.05); 
                margin-bottom: 16px;
                transition: transform 0.2s ease-in-out;
                cursor: pointer;
            " onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                <h4 style="margin-bottom: 8px;">{name.title()}</h4>
                <p style="margin: 4px 0; font-weight:500;">{specialty.title()}</p>
                <p style="margin: 4px 0;">{city.title()}, {state.title()}</p>
                <p style="margin: 4px 0; font-size: 18px;">{stars}</p>
                <p style="margin: 4px 0; font-size: 14px;">Rating: {rating}</p>
            </div>
        </a>
        """,
        unsafe_allow_html=True,
    )


# function to make 3 cards for each doctor
def create_doctor_cards():
    with data_placeholder:
        bdocs = st.session_state.search_results
        doc1 = bdocs.iloc[0]
        doc2 = bdocs.iloc[1]
        doc3 = bdocs.iloc[2]
        docs = [doc1, doc2, doc3]

        doc_cols = st.columns(3)
        for i in range(3):
            with doc_cols[i]:
                doc = docs[i]
                doctor_card(
                    name=doc["Doctor Name"],
                    specialty=doc["Specialty"],
                    city=doc["City"],
                    state=doc["State"],
                    rating=doc["Rating"],
                    profile_url="https://www.youtube.com",
                )


# Display the results if they exist
if st.session_state.search_results is not None:
    create_doctor_cards()


set_location_text_placeholder = st.empty()

if st.session_state.in_signup_process or st.session_state.logged_in:
    st.markdown(
        "Set or update your location in Profile Information and complete a chat in order to search for doctors."
    )
    if st.button("Go to Profile Information"):
        st.switch_page("pages/Profile_Information.py")
elif not st.session_state.logged_in:
    st.markdown("Please log in to search for doctors in your area.")
    if st.button("Log In"):
        st.switch_page("pages/Login.py")


# for state in st.session_state.items():
#     st.write(f"{state[0]}: {state[1]}")
