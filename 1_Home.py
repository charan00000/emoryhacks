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
    if len(report_info) > 0:
        make_csv(report_info, upload = True)
        print(specialty)
        #models.search_doctors(specialty)


def display_pdf(file_path = 'conversation.pdf'):
    images = convert_from_path(file_path)
    for image in images:
        st.image(image)

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

if st.button("Generate Report"):
    display_pdf()


# Search section
search_cols = st.columns((6, 1))
search_cols[0].markdown('<h2>Find the right doctor for you!</h2>', unsafe_allow_html=True)
search_cols[1].button("Search")

# Footer
st.markdown('<div class="footer">ReferAI - Your Health Assistant</div>', unsafe_allow_html=True)
