import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(
    page_title="StudyBuddy AI",
    page_icon="📚",
    layout="centered"
)

st.title("📚 StudyBuddy AI")
st.subheader("Your Personal AI Study Assistant")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API key missing! Please check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

notes = st.text_area(
    "📝 Paste Your Study Notes",
    height=250,
    placeholder="Paste your notes here..."
)

task = st.selectbox(
    "Choose what you want AI to do:",
    [
        "Summarize Notes",
        "Explain in Simple Language",
        "Generate Quiz",
        "Generate Important Questions"
    ]
)

if st.button("✨ Generate", use_container_width=True):

    if not notes.strip():
        st.warning("Please paste your study notes first.")

    else:
        prompts = {
            "Summarize Notes":
                "Summarize the following study notes into clear bullet points.",

            "Explain in Simple Language":
                "Explain the following notes in simple language with examples.",

            "Generate Quiz":
                "Create 5 practice quiz questions from these notes and provide answers.",

            "Generate Important Questions":
                "Generate 10 important exam practice questions from these notes."
        }

        with st.spinner("StudyBuddy AI is thinking..."):

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=(
                        prompts[task]
                        + "\n\nStudy notes:\n"
                        + notes
                    )
                )

                st.success("Your result is ready!")

                st.markdown("### 📖 Your Result")

                st.markdown(response.text)

            except Exception as e:
                st.error(
                    "AI request failed. Please check your API key, "
                    "internet connection, and API limits."
                )
                st.caption(f"Error: {e}")