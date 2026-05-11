from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import (HumanMessage,SystemMessage)

from dotenv import load_dotenv
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

# Memory / History

chat_history = [
    SystemMessage(content="You are a helpful AI assistant.")
]


while True:
    query = input("User: ")

    if query.lower() in ["exit","quit"]:
        break

    # Add user query to history
    chat_history.append(HumanMessage(content=query))

    # response = agent.invoke({
    #     "messages":[{"role":"user","content":query}]
    # })

    response = agent.invoke({
        "messages": chat_history
        })

    #Prints list of types of messages
    for msg in response["messages"]:
    #     print(f"{type(msg)} -> {msg}")
        print(type(msg).__name__)

    final_response = response["messages"][-1]

    # print(f"Final response type: {type(final_response), final_response}")
        
    print("\nAgent: ",final_response.content)

    # Save AI response to history
    chat_history.append(final_response)