import streamlit as st
import requests
import json

st.title("RAG Chat Application")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from RAG
    with st.chat_message("assistant"):
        try:
            response = requests.post(
                "http://localhost:3000/",
                json={"text": prompt}
            )
            if response.status_code == 200:
                # Debug the response
                print(f"Raw response: {response.text}")
                
                try:
                    # If it's JSON
                    response_data = response.json()
                    if isinstance(response_data, dict):
                        answer = response_data.get("result", response_data)
                    else:
                        answer = str(response_data)
                except json.JSONDecodeError:
                    # If it's not JSON, use the raw text
                    answer = response.text
            else:
                answer = f"Error: Received status code {response.status_code}"
        except requests.RequestException as e:
            answer = f"Error connecting to the server: {str(e)}"
            
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Sidebar with info
with st.sidebar:
    st.markdown("""
    ### About
    This is a RAG (Retrieval Augmented Generation) application built with:
    - Pathway
    - Ollama (Mistral)
    - Streamlit
    
    The app answers questions based on your documents while keeping everything private and local.
    """)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()