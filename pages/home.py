import streamlit as st
from dataclasses import dataclass
from typing import Literal
from ..gemeni import generate


st.set_page_config(page_title="ReferAI", layout="wide")

with open("statics/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)



# Header
st.markdown(
    """
    <style>
        .header {
            background-color: #2D4871;
            padding: 15px;
            color: white;
            font-size: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header a {
            color: white;
            margin: 0 10px;
            text-decoration: none;
        }
        .header-buttons {
            display: flex;
        }
        .chat-container {
            background-color: #2D4871;
            padding: 20px;
            border-radius: 10px;
            color: white;
        }
        .chat-bubble {
            background-color: #8796c2;
            padding: 15px;
            border-radius: 10px;
            display: inline-block;
            max-width: 80%;
        }
        .chat-bubble-user {
            background-color: #b8a5db;
            text-align: right;
        }
        .search-bar {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .footer {
            background-color: #2D4871;
            padding: 20px;
            color: white;
            text-align: center;
        }
    </style>
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
    
def on_click_callback():
    human_prompt = st.session_state.human_prompt
    llm_response = generate(human_prompt, st.session_state.history)
    st.session_state.history.append(Message("human", human_prompt))
    st.session_state.history.append(Message("ai", llm_response))
    # st.session_state.history.append(human_prompt)

initialize_session_state()

chat_container = st.container()
prompt_container = st.form("chat-form")
credit_card_placeholder = st.empty()

with chat_container:
    for chat in st.session_state.history:
        st.markdown(f'From {chat.origin}: {chat.message}')

with prompt_container:
    st.markdown("**ReferAI Medical Assistant** - _press Enter to send a message_")
    cols = st.columns((6, 1))
    cols[0].text_input(
        "Chat",
        placeholder='Symtoms, condtions, help...',
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
search_query = st.text_input("Search for a doctor", key="search")
st.button("Search")

# Footer
st.markdown('<div class="footer">ReferAI - Your Health Assistant</div>', unsafe_allow_html=True)
