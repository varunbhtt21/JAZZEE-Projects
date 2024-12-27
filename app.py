import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env
load_dotenv()

# Get the API key from environment variable
api_key = os.getenv("GENAI_API_KEY")
email_username = os.getenv("EMAIL_USERNAME")
email_password = os.getenv("EMAIL_PASSWORD")

if not api_key:
    st.error("Error: Gemini API key not found. Please set GENAI_API_KEY in your .env file.")
    st.stop()

# Configure the Gemini model
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_gemini(prompt: str) -> str:
    """Utility function to call the Gemini model and return the text response."""
    response = model.generate_content(prompt)
    return response.text

def send_email(to_email, subject, body):
    """Send an email using SMTP."""
    try:
        msg = MIMEMultipart()
        msg['From'] = email_username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_username, email_password)
            server.sendmail(email_username, to_email, msg.as_string())

        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# ------------------------------
# Streamlit App
# ------------------------------
st.title("Generative AI App with Gemini")

# Input field to accept user description
user_description = st.text_input("Enter a description or topic:")

# Initialize session state for generated content
if "generated_content" not in st.session_state:
    st.session_state.generated_content = ""

col1, col2, col3, col4 = st.columns(4)

# Button for Email
if col1.button("Email"):
    email_prompt = f"""
    You are an AI that writes professional emails. 
    Write a clear, concise, and polite email about the following:
    Topic/Description: "{user_description}"
    Make sure the email has a greeting, body, and a proper closing.
    """
    response = ask_gemini(email_prompt)
    st.subheader("Generated Email")
    st.write(response)
    st.session_state.generated_content = response

# Button for Research Paper
if col2.button("Research Paper"):
    research_paper_prompt = f"""
    You are an academic writer. Please write a research paper based on the description below.
    Use the following structure:
      1. Abstract
      2. Introduction
      3. Literature Review
      4. Methodology
      5. Results and Discussion
      6. Conclusion and Future Work

    Topic/Description: "{user_description}"

    Please ensure the final output is well-structured, formal, and detailed.
    """
    response = ask_gemini(research_paper_prompt)
    st.subheader("Generated Research Paper")
    st.write(response)
    st.session_state.generated_content = response

# Button for Shayari
if col3.button("Shayari"):
    shayari_prompt = f"""
    Write a beautiful Hindi shayari (short poem) based on the following topic/description:
    "{user_description}"
    Make it emotional, melodic, and captivating.
    """
    response = ask_gemini(shayari_prompt)
    st.subheader("Generated Shayari")
    st.write(response)
    st.session_state.generated_content = response

# Button for Joke
if col4.button("Joke"):
    joke_prompt = f"""
    You are a stand-up comedian. Please write a short, light-hearted joke related to:
    "{user_description}"
    Make it fun and witty.
    """
    response = ask_gemini(joke_prompt)
    st.subheader("Generated Joke")
    st.write(response)
    st.session_state.generated_content = response

# Email Functionality
st.write("---")
st.subheader("Send Generated Content via Email")
recipient_email = st.text_input("Enter recipient email address:")
if st.button("Send Email"):
    if recipient_email and st.session_state.generated_content:
        subject = "Generated Content from Generative AI App"
        if send_email(recipient_email, subject, st.session_state.generated_content):
            st.success(f"Email successfully sent to {recipient_email}")
    else:
        st.error("Please generate content and provide a valid email address.")
