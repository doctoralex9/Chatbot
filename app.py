import os
from openai import OpenAI
import streamlit as st
#for no need to login etc.
from dotenv import load_dotenv
load_dotenv()


#1st variable: "client", 2nd variable: "api_key"
client = OpenAI(api_key = os.environ["API_KEY"])

#2nd variable: "system_prompt"
system_prompt = "You are a helpful assistant that helps people debug their code."
if prompt := st.chat_input("What's your coding question?"):  # ← Replaces our old input("user_prompt")
    # Display user message in UI
    with st.chat_message("user"):
        st.markdown(prompt)
    
    
    chat_completion = client.responses.create(
        model="gpt-4o-mini",
        tools=[{"type": "web_search_preview"}], 
        input=prompt  
    )
    
    # Display AI response in UI
    with st.chat_message("assistant"):
        st.markdown(chat_completion.output_text)