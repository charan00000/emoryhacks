import streamlit as st
from dataclasses import dataclass
from typing import Literal
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gemini import generate
import base64
import models


st.set_page_config(page_title="ReferAI", layout="wide")

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
        <div class="header-buttons">
            <button>Log in</button>
            <button>Sign up</button>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Title
st.markdown("<h1><strong>The Right Doctor. The Right Time.</strong></h1>", unsafe_allow_html=True)


# chat section

@dataclass
class Message:
    origin: Literal["human", 'ai']
    message: str

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
        st.session_state.num_responses = 0
    
def on_click_callback():
    human_prompt = st.session_state.human_prompt
    llm_response = generate(human_prompt, st.session_state.history, st.session_state.num_responses)
    current_response = llm_response[0]
    report_info = llm_response[1]
    st.session_state.num_responses += 1
    st.session_state.history.append(Message("human", human_prompt))
    st.session_state.history.append(Message("ai", current_response))
    st.session_state.human_prompt = ""
    if len(report_info) > 0:
        models.update_report(report_info)

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




# Search section
st.markdown('<h2>Find the right doctor for you!</h2>', unsafe_allow_html=True)
st.button("Search")

# Footer
st.markdown('<div class="footer">ReferAI - Your Health Assistant</div>', unsafe_allow_html=True)
