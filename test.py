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

file = client.files.create(
    file=open(".test/tailwinddocs.pdf", "rb"),
         purpose="assistants" 
)

# step 1: create an assistant
assistant = client.beta.assistants.create(
    name="Miriko Web Master",
    instructions="""""
    You are an Expert Web Developer. 
    You are a part of team called Mikirinkode, 
    here you work together with other roles to build beautiful website using Tailwind.
    
    If you need image, use this link as src: https://raw.githubusercontent.com/mikirinkode/autonomous-ai-team/main/images/dummy/dummyimage.png
    adjust the image size to fit your need, and than add image alt with appropriate text about what should be displayed.
    
    You will be given commands to write HTML code with Tailwind,
    Then you will respond only with the code in HTML format.
    Remember you will only respond the code
    """.strip(),
    tools=[{"type": "retrieval"}],
    model="gpt-4-turbo-preview",
    file_ids=[file.id]
)

# step 2: create a thread
thread = client.beta.threads.create()

# step 3: add a message to a thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)

# step 4: run the assistant
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account."
)

# step 5: check the run status
run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)

# step 6: display the assistant's response
messages = client.beta.threads.messages.list(
  thread_id=thread.id
)