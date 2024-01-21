import streamlit as st
from agent import Agent
from openai import OpenAI

openai_model="gpt-3.5-turbo"
api_key=st.secrets["OPENAI_API_KEY"]
org_id=st.secrets["OPENAI_ORG_ID"]

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#
# Web
#
st.set_page_config(layout="centered", page_title="Autonomous GPT Team", page_icon=":robot_face:")
st.title("Autonomous GPT Team")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})