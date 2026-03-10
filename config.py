import streamlit as st

# Read API key from Streamlit Secrets
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")

MODEL_NAME = "gpt-4.1"
