import streamlit as st
import sqlite3
from streamlit_extras.switch_page_button import switch_page
from dataclasses import dataclass

st.set_page_config( layout="wide")
def load_css():
    with open("static/style.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

load_css()

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
def check_login(email, password):
	conn = sqlite3.connect("emory_hack.db")
	c = conn.cursor()
	c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
	data = c.fetchall()
	conn.close()
	if len(data) == 0:
		return False
	return True

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

  
  
  .poppins-regular {
    font-family: "Poppins", sans-serif;
    font-weight: 400;
    font-style: normal;
  }
  
  .poppins-semibold {
    font-family: "Poppins", sans-serif;
    font-weight: 600;
    font-style: normal;
  }
  
  .poppins-bold {
    font-family: "Poppins", sans-serif;
    font-weight: 700;
    font-style: normal;
  }

  .poppins-black {
    font-family: "Poppins", sans-serif;
    font-weight: 900;
    font-style: normal;
  }

  
  .poppins-regular-italic {
    font-family: "Poppins", sans-serif;
    font-weight: 400;
    font-style: italic;
  }

  
  .poppins-bold-italic {
    font-family: "Poppins", sans-serif;
    font-weight: 700;
    font-style: italic;
  }


* {
	box-sizing: border-box;
    font-family: "Poppins", sans-serif;
    font-style: normal;
}

body {
	background: #f6f5f7;
	display: flex;
	justify-content: center;
	align-items: center;
	flex-direction: column;
	height: 100vh;

}

h1 {
	font-weight: bold;
	margin: 0;
}

h2 {
	text-align: center;
}

p {
	font-size: 14px;
	font-weight: 100;
	line-height: 20px;
	letter-spacing: 0.5px;
	margin: 20px 0 30px;
}

span {
	font-size: 12px;
}

a {
	color: #333;
	font-size: 14px;
	text-decoration: none;
	margin: 15px 0;
}

button {
	border-radius: 20px;
	border: 1px solid #274C77;
	background-color: #274C77;
	color: #FFFFFF;
	font-size: 12px;
	font-weight: bold;
	padding: 12px 45px;
	letter-spacing: 1px;
	text-transform: uppercase;
	transition: transform 80ms ease-in;
}

button:active {
	transform: scale(0.95);
}

button:focus {
	outline: none;
}

button.ghost {
	background-color: transparent;
	border-color: #FFFFFF;
}

form {
	background-color: #FFFFFF;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
	padding: 0 50px;
	height: 100%;
	text-align: center;
}

input {
	background-color: #eee;
	border: none;
	padding: 12px 15px;
	margin: 8px 0;
	width: 100%;
}

.container {
	background-color: #274C77;
	border-radius: 10px;
  	box-shadow: 0 14px 28px rgba(0,0,0,0.25), 
			0 10px 10px rgba(0,0,0,0.22);
	position: absolute;
	overflow: hidden;
	width: 768px;
	max-width: 100%;
	min-height: 480px;
}

.form-container {
	position: absolute;
	top: 0;
	height: 100%;
	transition: all 0.6s ease-in-out;
}

.sign-in-container {
	left: 0;
	width: 50%;
	z-index: 2;
}

.container.right-panel-active .sign-in-container {
	transform: translateX(100%);
}

.sign-up-container {
	left: 0;
	width: 50%;
	opacity: 0;
	z-index: 1;
}

.container.right-panel-active .sign-up-container {
	transform: translateX(100%);
	opacity: 1;
	z-index: 5;
	animation: show 0.6s;
}

@keyframes show {
	0%, 49.99% {
		opacity: 0;
		z-index: 1;
	}
	
	50%, 100% {
		opacity: 1;
		z-index: 5;
	}
}

.overlay-container {
	position: absolute;
	top: 0;
	left: 50%;
	width: 50%;
	height: 100%;
	overflow: hidden;
	transition: transform 0.6s ease-in-out;
	z-index: 100;
}

.container.right-panel-active .overlay-container{
	transform: translateX(-100%);
}

.overlay {
	background: #274C77;
	background-repeat: no-repeat;
	background-size: cover;
	background-position: 0 0;
	color: #FFFFFF;
	position: relative;
	left: -100%;
	height: 100%;
	width: 200%;
  	transform: translateX(0);
	transition: transform 0.6s ease-in-out;
}

.container.right-panel-active .overlay {
  	transform: translateX(50%);
}

.overlay-panel {
	position: absolute;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-direction: column;
	padding: 0 40px;
	text-align: center;
	top: 0;
	height: 100%;
	width: 50%;
	transform: translateX(0);
	transition: transform 0.6s ease-in-out;
}

.overlay-left {
	transform: translateX(-20%);
}

.container.right-panel-active .overlay-left {
	transform: translateX(0);
}

.overlay-right {
	right: 0;
	transform: translateX(0);
}

.container.right-panel-active .overlay-right {
	transform: translateX(20%);
}

.social-container {
	margin: 20px 0;
}

.social-container a {
	border: 1px solid #DDDDDD;
	border-radius: 50%;
	display: inline-flex;
	justify-content: center;
	align-items: center;
	margin: 0 5px;
	height: 40px;
	width: 40px;
}
</style>
    """,
    unsafe_allow_html=True,
)
# st.markdown(
#     """
# <div class="container poppins-regular" id="container">
# 	<div class="form-container sign-up-container">
# 		<form action="#">
# 			<h1>Create Account</h1>
# 			<div class="social-container">
# 				<a href="#" class="social"><i class="fab fa-facebook-f"></i></a>
# 				<a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
# 				<a href="#" class="social"><i class="fab fa-linkedin-in"></i></a>
# 			</div>
# 			<span>or use your email for registration</span>
# 			<input type="text" placeholder="Name" />
# 			<input type="email" placeholder="Email" />
# 			<input type="password" placeholder="Password" />
# 			<button>Sign Up</button>
# 		</form>
# 	</div>
# 	<div class="form-container sign-in-container">
# 		<form action="#">
# 			<h1>Sign in</h1>
# 			<div class="social-container">
# 				<a href="#" class="social"><i class="fab fa-facebook-f"></i></a>
# 				<a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
# 				<a href="#" class="social"><i class="fab fa-linkedin-in"></i></a>
# 			</div>
# 			<span>or use your account</span>
# 			<input type="email" placeholder="Email" />
# 			<input type="password" placeholder="Password" />
# 			<a href="#">Forgot your password?</a>
# 			<button>Sign In</button>
# 		</form>
# 	</div>
# 	<div class="overlay-container">
# 		<div class="overlay">
# 			<div class="overlay-panel overlay-left">
# 				<h1>Welcome Back!</h1>
# 				<p>To keep connected with us please login with your personal info</p>
# 				<button class="ghost" id="signIn">Sign In</button>
# 			</div>
# 			<div class="overlay-panel overlay-right">
# 				<h1>Hello, Friend!</h1>
# 				<p>Enter your personal details and start journey with us</p>
# 				<button class="ghost" id="signUp">Sign Up</button>
# 			</div>
# 		</div>
# 	</div>
# </div>
#     """,
#     unsafe_allow_html=True,
# )

st.markdown("""
    <style>
        <style>
        /* Set the background color for the entire page */
        body {
            background-color: #f6f5f7;
            font-family: 'Arial', sans-serif;
        }

        /* Style the form container */
        .stContainer {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
        }

        /* Style the circular social buttons */
        .social-button {
            border: 1px solid #DDDDDD;
            border-radius: 50%;
            display: inline-flex;
            justify-content: center;
            align-items: center;
            margin: 20px 10px;
            height: 50px;
            width: 50px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .social-button:hover {
            transform: scale(1.1);
        }

        .google-button {
            background-color: #4285F4;
            color: white;
        }

        .microsoft-button {
            background-color: #00A4EF;
            color: white;
        }

        .google-button i, .microsoft-button i {
            font-size: 24px;
        }

        footer {
            background-color: #222;
            color: #fff;
            font-size: 14px;
            padding: 10px;
            text-align: center;
            position: fixed;
            bottom: 0;
            width: 100%;
        }

        footer a {
            color: #3c97bf;
            text-decoration: none;
        }
    </style>
""", unsafe_allow_html=True)

login, signup = st.tabs(["Login", "Sign Up"])

st.markdown(
	"""
	<style>

	
	[data-testid="stForm"] {
    	background-color: #274C77;
		box-shadow: 0 14px 28px rgba(0,0,0,0.25), 
			0 10px 10px rgba(0,0,0,0.22);
	}	

	[data-testid="stBaseButton-secondaryFormSubmit"] {
    	background-color: #F8F9FA;
	}	
	.st-af {
    	font-size:24px;
	}	

	em {
		color: #F8F9FA;
	}
	strong {
		color: #274C77;
	}

	h3 {
	    text-align: center;
	    color: #274C77;
		
	}
</style>
""", unsafe_allow_html=True)

with login:

	with st.form("login-form", clear_on_submit=True, border=True) as login_form:
		email = st.text_input("*Email*", key="email-text")
		password = st.text_input("*Password*", key="password-text")
		submitted = st.form_submit_button("**Log in**",type="secondary")
		if submitted and check_login(email, password):
			st.write(email, password,)
			st.success("Login successful!")
			switch_page("Home")
		elif submitted:
			st.write('Login failed')
with signup:
	with st.form("signup-form", clear_on_submit=True, border=True) as login_form:
		email = st.text_input("*Email*", key="email-text2", placeholder="Email")
		password = st.text_input("*Password*", key="password-text2", placeholder="Password")
		verify_password = st.text_input("*Verify Password*", key="verify-password-text", placeholder="Type your password again")
		submitted = st.form_submit_button("**Sign up**",type="secondary")
		if submitted:
			conn = sqlite3.connect("emory_hack.db")
			c = conn.cursor()
			c.execute("SELECT * FROM users WHERE email = ?", (email,))
			existing_user = c.fetchone()
			if existing_user:
				st.error("User already exists")
			else:
				#signup logic here
				st.session_state.current_user.email = email
				st.session_state.current_user.password = password
				if password != verify_password:
					st.error("Passwords do not match")
				else:
					st.write(email, password,)
					st.success("Signup successful!")
					switch_page("profile information")
bar, text, bar = st.columns(3)
st.markdown("""
	<h3>- OR -</h3>
""", unsafe_allow_html=True)



