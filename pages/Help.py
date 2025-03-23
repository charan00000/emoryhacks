import streamlit as st

LOGO = "static/emory_hack_logo.png"

with open("static/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st.logo(LOGO, icon_image=LOGO, size="large")
# Page title
st.title("🤖 Help — How to Use ReferAI")
st.write("Welcome to **ReferAI**, your smart medical assistant designed to help you find the right doctor at the right time. Here’s how our platform works and how you can make the most of it:")

# Step 1
st.header("1️⃣ Start with Your Symptoms")
st.write("""
On the home page, you’ll find a chat box where you can describe:
- Your current symptoms
- How long you’ve been experiencing them

Our AI chatbot — trained on evidence-based diagnostic algorithms — will analyze this information and provide a preliminary diagnosis suggestion. This helps prescreen patients efficiently, reducing the manual work for nurses and doctors.
""")

# Step 2
st.header("2️⃣ Get Matched with the Right Specialist")
st.write("""
Based on your symptoms, we’ll recommend the most relevant medical specialty. No more guessing who to see — our system guides you to the right expert from the start.
""")

# Step 3
st.header("3️⃣ Find Doctors Near You")
st.write("""
You can then:
- Set a travel radius based on how far you're willing to go
- See a list of available doctors in that area
""")



# Need Assistance
st.subheader("🔎 Need Assistance?")
st.write("""
If you need help at any point, feel free to reach out to us using the **Connect With Us** link at the top of the page or visit the **About** section to learn more.
""")

st.markdown("> We’re here to make your healthcare journey smoother, faster, and smarter.")

# Optional nice touch: Footer
st.write("---")
st.write("👉 **Ready to start? Head back to the main page and chat with ReferAI!**")


