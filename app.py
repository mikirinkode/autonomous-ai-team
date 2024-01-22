import streamlit as st
from agent import Agent
from openai import OpenAI
from utils import *
from feature import FeatureStatus
import json
        
openai_model="gpt-4"
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
    Then, you have to create a json list of features that should be implemented in the website.
    Each Feature represent one html file, atleast should have a main feature or main page with html file name as "home.html"
    
    please return in this JSON list format:
    [
        {"feature": "Create Home Page with Responsive Design, clear and concise content, attractive and modern layout, eye-catching hero section, navigaiton menu, contact information, call to action section, social media integration, testimonial section, responsive iamges, footer with relevant links", html_file_name: "home.html", "status": "-"},
        {"feature": "feature1", html_file_name: "feature1.html", "status": "-"},
        {"feature": "feature2", html_file_name: "feature2.html", "status": "-"},
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
    
    If you need image, use this link as src: https://raw.githubusercontent.com/mikirinkode/autonomous-ai-team/main/images/dummy/dummyimage.png
    adjust the image size to fit your need, and than add image alt with appropriate text about what should be displayed.
    
    You will be given commands to write HTML code with Tailwind,
    Then you will respond only with the code in HTML format.
    Remember you will only respend the code
    """.strip(),
    openai_client=client,
    openai_model=openai_model
)

agents = [project_manager_agent, web_dev_agent]

project_name = ""
project_detail = ""

if "features" not in st.session_state:
    st.session_state.features = []

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
        if message["role"] == web_dev_agent.name:
            with st.expander("Code"):
                st.code(message["content"])
        elif message["role"] == project_manager_agent.name:
            st.code(message["content"])
        else:
            st.markdown(message["content"])

with st.sidebar:
    st.subheader("Project Details")
    for feature in st.session_state.features:
        st.checkbox(feature.feature, value=feature.status != "-", disabled = True)

# if features is not empty
if len(st.session_state.features) > 0:
    # check if there is a status is not complete
    is_not_complete = any(feature.status == "-" for feature in st.session_state.features)

    if (is_not_complete):
        for feature in st.session_state.features:
        
            content =f"Project Manager assign '{feature.feature}' to Web Developer" 
            st.write(content)
            st.session_state.messages.append({"role": project_manager_agent.name, "content": content})
            
            if feature.status == "-":
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    
                    for response in web_dev_agent.chat(prompt=feature.feature):
                        full_response += (response.choices[0].delta.content or "")
                        message_placeholder.code(full_response + "▌")
                    
                    message_placeholder.code(full_response)
                    
                    html_content = full_response
                    create_html_file(feature.html_file_name, html_content)
                        
                st.session_state.messages.append({"role": web_dev_agent.name, "content": full_response})
                new_feature = FeatureStatus(feature.feature, feature.html_file_name, "DONE")
                st.session_state.features[st.session_state.features.index(feature)] = new_feature
                
    else :
        with st.container(border=True):
            st.write("ALL FEATURES DONE")
            st.write("Feature List:")
            for feature in st.session_state.features:
                if feature.status != "-":
                    st.write("✅", feature.feature)
            
# if features is empty, thatn Accept user input
elif prompt := st.chat_input("What is up?"):
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
            
            # ProjectFeature = namedtuple('ProjectFeature', ['feature', 'status'])
            st.session_state.features = [FeatureStatus(feature["feature"], feature["html_file_name"], feature["status"]) for feature in json.loads(full_response)]
            
            message_placeholder.code(full_response)
        
    st.session_state.messages.append({"role": selected_agent, "content": full_response})
    