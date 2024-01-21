import streamlit as st
from agent import Agent
from openai import OpenAI
from utils import *

openai_model="gpt-3.5-turbo"
api_key=st.secrets["OPENAI_API_KEY"]
org_id=st.secrets["OPENAI_ORG_ID"]

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

project_manager_agent = Agent(
    agent_name="project-manager",
    agent_skills="""
    You are an Expert Project Manager. 
    You are a part of team called Mikirinkode, 
    here you work together with other roles to build beautiful website.
    You will be given a website idea,
    Then, you have to create a json list of features that should be implemented in the website
    
    please return in this JSON list format:
    [
        {"feature": "feature1", "status": "-"},
        {"feature": "feature2", "status": "-"},
    ]
    """.strip(),
    openai_client=client,
    openai_model=openai_model
)

web_dev_agent = Agent(
    agent_name="web-dev",
    agent_skills="""
    You are an Expert Web Developer. 
    You are a part of team called Mikirinkode, 
    here you work together with other roles to build beautiful website using Tailwind.
    You will be given commands to write HTML code with Tailwind,
    Then you will respond only with the code in HTML format.
    Remember you will only respend the code
    """.strip(),
    openai_client=client,
    openai_model=openai_model
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#
# Web
#
st.set_page_config(layout="centered", page_title="Autonomous AI Team", page_icon=":robot_face:")
st.title("Autonomous AI Team")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    selected_agent = message["role"]
    st.write(selected_agent, ": ")
    
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    selected_agent = project_manager_agent.name
    
    st.write("Selected agent:", selected_agent)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        if selected_agent == project_manager_agent.name:
            for response in project_manager_agent.chat(prompt=prompt):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.code(full_response + "▌")
            
            message_placeholder.code(full_response)
        
        elif selected_agent == web_dev_agent.name:
            for response in web_dev_agent.chat(prompt=prompt):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.code(full_response + "▌")
            
            message_placeholder.code(full_response)
            
            html_content = full_response
            create_html_file("web-dev", html_content)
            
    st.session_state.messages.append({"role": selected_agent, "content": full_response})
    