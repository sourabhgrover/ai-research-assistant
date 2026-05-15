from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"),model_name=os.getenv("MODEL_NAME"))

response = llm.stream('What is RAG')

for chunk in response:
    print(chunk.content,end="",flush=True)