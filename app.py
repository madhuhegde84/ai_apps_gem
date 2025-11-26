import streamlit as st
import google.generativeai as genai

# Page configuration
st.title("🤖 My Gemini AI App")
st.write("Ask me anything about embedded systems, WiFi, or anything else!")

# Get API key from Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# User input
prompt = st.text_area("Enter your question:", height=100)

# Generate button
if st.button("Generate Response"):
    if prompt:
        with st.spinner("Thinking..."):
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            st.success("Response:")
            st.write(response.text)
    else:
        st.warning("Please enter a question first!")