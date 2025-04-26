import streamlit as st
from agent import query_data_with_agent
from data_handler import handle_file_upload

st.set_page_config(page_title="📊 AI Data Analysis Agent", layout="wide")
st.title("📊 AI Data Analysis Agent")

# Sidebar for API Key
api_key = st.sidebar.text_input("🔐 Enter your OpenAI API key", type="password").strip()

# Session State to store file upload status
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False

# Upload File
uploaded_file = st.file_uploader("📤 Upload a CSV or Excel file", type=["csv", "xlsx"])

# After upload
if uploaded_file and not st.session_state.file_uploaded:
    handle_file_upload(uploaded_file)
    st.session_state.file_uploaded = True
    st.success("✅ File loaded successfully!")

# If file uploaded already, allow asking questions
if st.session_state.file_uploaded:
    st.subheader("💬 Ask questions about your data")

    query = st.text_input("Type your question here:")

    if st.button("Submit") and query and api_key:
        with st.spinner("Processing your query..."):
            response = query_data_with_agent(api_key, "uploaded_data", query)
            st.markdown(response['answer'])
            if 'df' in response:
                st.dataframe(response['df'])
else:
    st.info("👆 Please upload a file first to start asking questions.")
