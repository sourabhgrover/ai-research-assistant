from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import (HumanMessage,SystemMessage)
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from dotenv import load_dotenv
import os

# =========================
# LOAD ENV
# =========================

load_dotenv()

# =========================
# LOAD LLM
# =========================
llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")

# =========================
# LOAD PDF
# =========================

loader = PyPDFLoader("doc/sample.pdf")

docs = loader.load()

# =========================
# SPLIT CHUNKS
# =========================

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

chunks = splitter.split_documents(docs)

print(f"Total Chunks: {len(chunks)}")


# =========================
# EMBEDDINGS
# =========================

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#=========================
# STORE IN VECTOR DB
#=========================
vector_store = Chroma.from_documents(documents=chunks, embedding=embedding)


# =========================
# RETRIEVER
# =========================

retriever = vector_store.as_retriever()


# =========================
# TOOLS
# =========================
# Tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@tool
def retrieve_docs(query:str) -> str:
    """Search and return relevant document chunks."""
    results = retriever.invoke(query)
    # return results
    return "\n\n".join([result.page_content for result in results])

# =========================
# AGENT
# =========================

agent = create_agent(model=llm,tools=[multiply,retrieve_docs])

# =========================
# MEMORY
# =========================

chat_history = [
    SystemMessage(content=(
        "You are a helpful AI assistant."
        "Use tools whenever required."
        )
    )
]

# =========================
# CHAT LOOP
# =========================

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