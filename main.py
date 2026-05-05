from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool
import os

# Load .env
load_dotenv()

# LLM
llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")

# Tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

#Agent
agent = create_agent(model=llm,tools=[multiply])


while True:
    query = input("User: ")

    if query.lower() in ["exit","quit"]:
        break

    response = agent.invoke({
        "messages":[{"role":"user","content":query}]
    })

    #Prints list of types of messages
    # for msg in response["messages"]:
    #     print(f"{type(msg)} -> {msg}")
        
    print("Agent: ",response["messages"][-1].content)