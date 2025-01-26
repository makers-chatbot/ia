import streamlit as st
import asyncio
import json
import uuid
import httpx
from typing import Dict

# Page config
st.set_page_config(
    page_title="Computer Inventory Chat", page_icon="💻", layout="centered"
)

# Constants
LANGCHAIN_SERVER_URL = "http://localhost:8001/chat"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


async def send_message(message: str) -> Dict:
    """Send message to LangChain server"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                LANGCHAIN_SERVER_URL,
                json={"session_id": st.session_state.session_id, "message": message},
                timeout=30.0,
            )
            response.raise_for_status()
            return {"response": response.json()["message"]}
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return {"response": "Sorry, I'm having trouble connecting to the server."}


# UI Elements
st.title("💻 AIda - Computer Inventory Assistant")
st.caption("How can I help you find the perfect computer?")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])  # Using markdown for better formatting

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    with st.chat_message("assistant"):
        response = asyncio.run(send_message(prompt))
        st.session_state.messages.append(
            {"role": "assistant", "content": response["response"]}
        )
        st.markdown(response["response"])
