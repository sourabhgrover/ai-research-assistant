from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools import tool

# =========================
# 1. LOAD PDF
# =========================
loader = PyPDFLoader("doc/sample.pdf")

docs = loader.load()

# print(docs[0].page_content)
# =========================
# 2. SPLIT  DOCUMENT INTO CHUNKS
# =========================

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

chunks = splitter.split_documents(docs)
# print("\n========== FIRST CHUNK ==========\n")
# print(chunks[0].page_content)

# print("\n========== TOTAL CHUNKS ==========\n")
print(len(chunks))

# =========================
# 3. CREATE EMBEDDINGS
# =========================

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# =========================
# 4. STORE IN VECTOR DB
# =========================

from langchain_community.vectorstores import Chroma

vectorstore = Chroma.from_documents(documents=chunks,embedding=embeddings)

# =========================
# 5. CREATE RETRIEVER
# =========================

retriever = vectorstore.as_retriever()

# =========================
# 6. ASK QUESTIONS
# =========================

while True:
    query = input("Enter your question (or 'exit' to quit): ")

    if query.lower() in ["exit","quit"]:
        break

    results = retriever.invoke(query)

    print("\n========== RETRIEVED CHUNKS ==========\n")
    for index,result in enumerate(results):
        print(f"Chunk {index+1}: {result.page_content}\n")

@tool
def retrive_docs(query: str) -> str:
    """Search and return relevant document chunks"""
    result =  retriever.invoke(query)

    return 
# # Step 6 Ask a question and retrieve relevant chunks
# query = "What is DOB of Kohli?"
# results = retriever.invoke(query)

# print(results[0].page_content)