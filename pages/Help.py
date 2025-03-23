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

# Step 4
st.header("4️⃣ Sort by What Matters to You")
st.write("""
We understand that preferences vary. That’s why you can sort doctors by:
- **Availability**
- **Ratings**
- Assign priority weights (for example, rate “availability” as more important than “rating,” or vice versa).
""")

# Step 5
st.header("5️⃣ Book and Sync Effortlessly")
st.write("""
Once you’ve found the right doctor and selected an appointment date:
- We create a secure database entry
- This is sent through our scheduling pipeline to keep both our system and the clinic’s database in sync
- We’ll also automatically update the calendars of both you and your doctor — if calendars are linked — so no one misses a thing
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


