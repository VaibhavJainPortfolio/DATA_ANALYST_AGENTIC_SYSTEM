import streamlit as st
from agent import query_data_with_agent
from data_handler import handle_file_upload

st.set_page_config(page_title="📊 AI Data Analysis Agent", layout="wide")
st.title("📊 AI Data Analysis Agent")

api_key = st.sidebar.text_input("🔐 Enter your OpenAI API key", type="password")

uploaded_file = st.file_uploader("📤 Upload a CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file:
    table_name = handle_file_upload(uploaded_file)
    st.success(f"✅ File loaded as table `{table_name}`")
    
    query = st.text_input("💬 Ask a question about your data:")
    
    if st.button("Submit") and query and api_key:
        with st.spinner("Processing..."):
            response = query_data_with_agent(api_key, table_name, query)
            st.write(response['answer'])
            if 'df' in response:
                st.dataframe(response['df'])
