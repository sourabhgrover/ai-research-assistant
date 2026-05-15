from fastapi import FastAPI
from pydantic import BaseModel

from dotenv import load_dotenv
import os

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq

#=====================
# LOAD ENV
#=====================

load_dotenv()

#==========================
# FASTAPI APP
#==========================

app = FastAPI(
    title="AI Reasearch Assistant"
)

#=================
# LLM
#=================

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name=os.getenv("MODEL_NAME")
    )

#==============
#TOOL
#===============

@tool
def multiply(a:int,b:int) -> int:
    """Multiply two numbers"""
    return a * b

#==================
# AGENT
#==================

agent = create_agent(model=llm,tools=[multiply])

#==================
# REQUEST MODEL
#==================

class ChatRequest(BaseModel):
    message : str
    
#==================
# RESPONSE MODEL
#==================

class ChatResponse(BaseModel):
    answer: str

@app.post("/chat",response_model=ChatResponse)
def chat(request:ChatRequest):

    response = agent.invoke({
        "messages":[{
            "role": "user",
            "content": request.message
        }
        ]
    })

    final_answer = response["messages"][-1].content

    return ChatResponse(answer=final_answer)