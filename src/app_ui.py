import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/query")

st.set_page_config(page_title="CSV Q&A Agent", layout="wide")
st.title("CSV Q&A Agent")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

question = st.text_input("Ask a question about your data:")

use_sample = st.checkbox("Use sample data.csv (if no file uploaded)", value=True)

if st.button("Submit") and question:
    with st.spinner("Thinking..."):
        try:
            files = {"file": uploaded_file} if uploaded_file else None
            payload = {"question": question, "use_sample": use_sample}
            response = requests.post(API_URL, data=payload, files=files)
            response.raise_for_status()
            answer = response.json().get("answer", "")
        except Exception as e:
            st.error(f"Error querying the API: {e}")
            answer = None
    if answer:
        st.subheader("Answer")
        st.write(answer)
