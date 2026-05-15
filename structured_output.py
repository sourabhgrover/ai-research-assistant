from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

class AnswerResponse(BaseModel):
    answer: str
    topic: str


llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name=os.getenv("MODEL_NAME")
    )

structured_llm = llm.with_structured_output(AnswerResponse)

response = structured_llm.invoke("Explain RAG in one line")

print(response)
