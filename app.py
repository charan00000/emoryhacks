import streamlit as st

from helper_methods import Person

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "in_signup_process" not in st.session_state:
    st.session_state.in_signup_process = False


# logout page
# resets session state to logged out and clears user data when logged out
def logout():
    st.session_state.logged_in = False
    st.session_state.in_signup_process = False
    st.session_state.current_user = Person("", "", "", "", "", "", "")
    st.session_state.human_prompt = ""
    st.session_state.specialty = ""
    st.session_state.search_results = None
    st.session_state.num_responses = 0
    st.session_state.history = []
    st.session_state.chatbot_error_message = ""
    st.switch_page("pages/Home.py")
    st.rerun()


def continue_signup():
    st.switch_page("pages/Profile_Information.py")


viewable = st.session_state.logged_in or st.session_state.in_signup_process

home_page = st.Page("pages/Home.py", title="Home", icon=":material/home:", url_path="#")
about_page = st.Page(
    "pages/About.py", title="About", icon=":material/groups:", url_path="about"
)
help_page = st.Page(
    "pages/Help.py", title="Help", icon=":material/help:", url_path="help"
)
login_page = st.Page(
    "pages/Login.py", title="Login", icon=":material/login:", url_path="login"
)
profile_info_page = st.Page(
    "pages/Profile_Information.py",
    title="Profile Information",
    icon=":material/account_circle:",
    url_path="profile-info",
    default=viewable,
)
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
continue_signup_page = st.Page(
    continue_signup, title="Continue Signup", icon=":material/how_to_reg:"
)


default_pages = [home_page, about_page, help_page]

page_dict = {"": default_pages}
account_pages = {"Account": []}

if not viewable:
    account_pages["Account"].append(login_page)
else:
    account_pages["Account"].append(profile_info_page)
    if st.session_state.logged_in:
        account_pages["Account"].append(logout_page)
    else:
        account_pages["Account"].append(continue_signup_page)

pg = st.navigation(page_dict | account_pages, position="sidebar", expanded=True)
pg.run()
