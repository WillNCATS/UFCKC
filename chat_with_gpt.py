

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env file
#!pip install python-dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()


def chat_with_gpt(messages):
    completion = client.chat.completions.create(
  model="gpt-4-turbo-preview",
  messages=messages
)
    return completion.choices[0].message





import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import shelve

# Load environment variables
load_dotenv()

# Streamlit app title
st.title("Chat with GPT")

# Assign avatars for the user and the bot
USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-turbo-preview"

# Function to load chat history
def load_chat_history():
    with shelve.open("chat_history.db") as db:
        return db.get("messages", [])

# Function to save chat history
def save_chat_history(messages):
    with shelve.open("chat_history.db") as db:
        db["messages"] = messages

# Load or initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Sidebar to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

# Display chat history
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.container():
        st.write(f"{avatar} {message['content']}")

# Function to handle chat interactions and call the OpenAI API
def interact_with_openai(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=st.session_state["messages"]
    )
    response_content = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": response_content})

    save_chat_history(st.session_state.messages)
    return response_content

# Chat input for user messages
if prompt := st.text_input("You:", key="prompt"):
    if st.button("Send"):
        bot_response = interact_with_openai(prompt)
        st.write(f"{BOT_AVATAR} {bot_response}")

# Save chat history after the interaction
save_chat_history(st.session_state.messages)
