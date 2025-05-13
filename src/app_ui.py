import streamlit as st
import requests
import pandas as pd
from io import BytesIO
from rag.config import API_URL, CSV_PATH

st.set_page_config(layout="wide")
st.title("Talk to Your CSV ")

# --- 0. Initialize session state flags on first run ---
if "indexed" not in st.session_state:
    st.session_state.indexed = False
if "index_requested" not in st.session_state:
    st.session_state.index_requested = False
if "use_sample" not in st.session_state:
    st.session_state.use_sample = None
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# --- Sidebar: Data Selection & Indexing ---
with st.sidebar:
    st.header("1. Load Your Data")
    sample_tab, upload_tab = st.tabs(["📄 Sample Data", "📤 Upload CSV"])

    # Sample Data tab
    with sample_tab:
        st.markdown(
             """
            **Use our sample dataset** to try out the Q&A agent immediately.
            
            - **Rows:** 30  
            - **Columns:** `Year Experience`, `Salary`  
            """
        )
        sample_df = pd.read_csv(CSV_PATH)
        st.dataframe(sample_df.head(5), use_container_width=True)

        if st.button("Index Sample Data"):
            st.session_state.use_sample = True
            st.session_state.uploaded_file = None
            st.session_state.index_requested = True

    # Upload CSV tab
    with upload_tab:
        uploaded = st.file_uploader("Select a CSV file", type="csv", key="uploader")
        if uploaded:
            st.success(f"Loaded `{uploaded.name}` — {uploaded.size/1024:.1f} KB")
            if st.button("Index Uploaded CSV"):
                st.session_state.use_sample = False
                st.session_state.uploaded_file = uploaded
                st.session_state.index_requested = True

# --- 2. Trigger indexing only when requested ---
if st.session_state.index_requested:
    with st.spinner("Indexing data… this may take a moment"):
        files = None
        if not st.session_state.use_sample:
            f = st.session_state.uploaded_file
            files = {"file": (f.name, f.getvalue(), "text/csv")}
        resp = requests.post(
            f"{API_URL}/index",
            data={"use_sample": st.session_state.use_sample},
            files=files
        )
        if resp.ok:
            info = resp.json()
            st.sidebar.success(f"✅ Indexed {info['num_docs']} rows")
            st.session_state.indexed = True
        else:
            st.sidebar.error(f"Indexing failed: {resp.text}")
        # Reset the trigger so it doesn't rerun
        st.session_state.index_requested = False

# --- 3. Main: Query Interface (once indexed) ---
if st.session_state.indexed:
    st.header("2. Ask a Question")
    question = st.text_input("Enter your question about the data:")
    if st.button("Submit") and question:
        with st.spinner("Thinking…"):
            resp = requests.post(
                f"{API_URL}/query",
                data={"question": question}
            )
            if resp.ok:
                answer = resp.json().get("answer", "")
                st.subheader("Answer")
                st.markdown(answer)
            else:
                st.error(f"Query failed: {resp.text}")
