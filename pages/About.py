import streamlit as st

LOGO = "static/emory_hack_logo.png"

st.set_page_config(page_title="About Us - ReferAI", layout="wide")

with open("static/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st.logo(LOGO, icon_image=LOGO, size="large")
import streamlit as st


st.title("🚀 About the Team Behind ReferAI")
st.write("""
At ReferAI, we’re a group of passionate students from top Georgia universities, united by a shared goal: to revolutionize the way patients connect with the right doctors.   
Our team blends diverse skills in data science, computer engineering, and software development — all dedicated to building smarter healthcare solutions.
""")

# Christo A
st.header("👨‍💻 Christo A")
st.subheader("Georgia State University | Freshman | Pre-CIS → Industrial Engineering (Georgia Tech Transfer Pathway)")
st.write("""
Christo is an aspiring data analyst and data scientist with a strong curiosity for solving complex problems with clean, insightful data visualizations.   
He is driven by a passion for using analytics to bridge gaps between people and solutions — whether it’s in healthcare, business, or technology.   
In his free time, you’ll find him learning new machine learning techniques, working on side projects, and exploring ways to make systems more efficient.
""")

# Charan K
st.header("💻 Charan K")
st.subheader("Georgia Tech | Freshman | Computer Science Major")
st.write("""
Charan is an aspiring data scientist who loves uncovering stories hidden in data.   
With a focus on building intelligent models and finding patterns others miss, he is passionate about using data to drive real-world change.   
Outside of coding, Charan enjoys participating in hackathons and is constantly on the lookout for innovative ways to use AI for good.
""")

# Bahuliya M
st.header("🖥️ Bahuliya M")
st.subheader("Georgia Tech | Freshman | Computer Science Major")
st.write("""
Bahuliya is a driven future software engineer with a knack for full-stack development and system design.   
She’s passionate about building applications that make a tangible difference in people's lives.   
Bahuliya thrives in collaborative environments and loves bringing technical ideas from concept to reality — with plenty of creativity in between.
""")

# Kedarnath M
st.header("🚀 Kedarnath M")
st.subheader("University of Georgia | Freshman | Computer Engineering Major")
st.write("""
Kedarnath is an aspiring aerospace engineer with a deep fascination for both the skies and the systems that power them.   
He brings a problem-solving mindset and technical rigor to every project, whether it’s building robust backend infrastructure or dreaming up future aerospace technologies.   
He’s the team’s resident ‘big thinker,’ always looking at how technology today can shape tomorrow’s world.
""")

st.markdown("---")
st.write("Together, we are **ReferAI** — using smart technology to make smarter healthcare connections.")
st.write("👉 Want to connect with us? Reach out through the **Connect With Us** page!")



