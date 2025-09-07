import os
from openai import OpenAI
#for no need to login etc.
from dotenv import load_dotenv
load_dotenv()


#1st variable: "client", 2nd variable: "api_key"
client = OpenAI(api_key = os.environ["API_KEY"])

#3rd variable: "system_prompt"
system_prompt = "You are a helpful assistant that helps people debug their code."

#4th variable: "user_prompt"
user_prompt = input("What's your question ? ")

#5th variable "chat_completion", passing to OpenAI's API, my system_promt and my user_prompt
chat_completion = client.chat.completions.create(
    #1st parameter
    messages =[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt} 
    ],

    #2nd parameter
    model = "gpt-5"
) 

#6th variable "response_text"
response_text = chat_completion.choices[0].message.content
print(response_text)