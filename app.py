import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
from supabase import create_client

# Load environment variables
load_dotenv()

# Supabase connection
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# OpenAI connection
client = OpenAI(api_key=os.environ["API_KEY"])

# System prompt
system_prompt = "You are a helpful assistant that helps people debug their code."

st.title("💬 AI Debugging Assistant")
st.write("Ask me anything about your code, and I'll try to help!")

# Handle user input
if prompt := st.chat_input("What's your coding question?"):
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    chat_completion = client.responses.create(
        model="gpt-4o-mini",
        tools=[{"type": "web_search_preview"}],
        input=prompt
    )

    response = chat_completion.output_text

    # Show AI response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Save chat into Supabase
    supabase.table("chat_history").insert({
        "user_id": "guest",  # TODO: replace with real user from Supabase Auth later
        "prompt": prompt,
        "response": response
    }).execute()

# Show chat history
st.subheader("📜 Your Chat History")
chats = supabase.table("chat_history").select("*").eq("user_id", "guest").order("id").execute()

for c in chats.data:
    st.write(f"**You:** {c['prompt']}")
    st.write(f"**Bot:** {c['response']}")
    with st.expander("⚙️ Manage this chat"):
        if st.button("❌ Delete", key=f"delete_{c['id']}"):
            supabase.table("chat_history").delete().eq("id", c["id"]).execute()
            st.rerun()
        if st.button("✏️ Update (test)", key=f"update_{c['id']}"):
            supabase.table("chat_history").update({"response": "Updated answer"}).eq("id", c["id"]).execute()
            st.rerun()
