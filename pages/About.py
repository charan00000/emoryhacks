import streamlit as st
from helper_methods import load_css

LOGO = "static/emory_hack_logo.png"

st.set_page_config(
    page_title="About Us - ReferAI",
    layout="wide",
    page_icon=LOGO
    )

load_css()

st.logo(LOGO, icon_image=LOGO, size="large")

st.title("🚀 About the Team Behind ReferAI")
st.write("""
At ReferAI, we’re a group of passionate students from top Georgia universities, united by a shared goal: to revolutionize the way patients connect with the right doctors.   
Our team blends diverse skills in data science, computer engineering, and software development — all dedicated to building smarter healthcare solutions.
""")

# Christo Antony
st.header("👨‍💻 Christo Antony")
st.subheader("Georgia State University | Freshman | Pre-CIS → Industrial Engineering (Georgia Tech Transfer Pathway)")
st.write("""
Christo is an aspiring data analyst and data scientist with a strong curiosity for solving complex problems with clean, insightful data visualizations.   
He is driven by a passion for using analytics to bridge gaps between people and solutions — whether it’s in healthcare, business, or technology.   
In his free time, you’ll find him learning new machine learning techniques, working on side projects, and exploring ways to make systems more efficient.
""")

# Charan Koyaguri
st.header("💻 Charan Koyaguri")
st.subheader("Georgia Tech | Freshman | Computer Science Major")
st.write("""
Charan is an aspiring data scientist who loves uncovering stories hidden in data.   
With a focus on building intelligent models and finding patterns others miss, he is passionate about using data to drive real-world change.   
Outside of coding, Charan enjoys participating in hackathons and is constantly on the lookout for innovative ways to use AI for good.
""")

# Bahuliya Manyapu
st.header("🖥️ Bahuliya Manyapu")
st.subheader("Georgia Tech | Freshman | Computer Science Major")
st.write("""
Bahuliya is a driven future software engineer with a knack for full-stack development and system design.   
She’s passionate about building applications that make a tangible difference in people's lives.   
Bahuliya thrives in collaborative environments and loves bringing technical ideas from concept to reality — with plenty of creativity in between.
""")

# Kedarnath Mohan
st.header("🚀 Kedarnath Mohan")
st.subheader("University of Georgia | Freshman | Computer Engineering Major")
st.write("""
Kedarnath is an aspiring aerospace engineer with a deep fascination for both the skies and the systems that power them.   
He brings a problem-solving mindset and technical rigor to every project, whether it’s building robust backend infrastructure or dreaming up future aerospace technologies.   
He’s the team’s resident ‘big thinker,’ always looking at how technology today can shape tomorrow’s world.
""")



st.markdown("---")
st.subheader("DISCLAIMER")
st.write("""
    This app was built as a personal project and is not a substitute for professional medical advice, 
    diagnosis, or treatment. By using this app, you acknowledge and agree that the creators of this project 
    are not responsible for any outcomes or actions taken based on the information provided. 
         
    Additionally, the doctors recommended by our service are not currently intended to be legitimate or 
    real medical professionals. We assume no responsibility for any potential defamation of any individuals 
    who may be coincidentally represented by our generated data.
""")




