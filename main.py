# import os
# # import qdrant_client 
# # import langchain_huggingface 
# # import langchain community 
# # import langchain-qdrant 
# # import pypdf 
# # import openai 
# # import langchain 
# # import transformers 
# # import langchain_huggingface 
# # import langchain_openai

# def get_relevant_docs(query, documents):
#     # Simple keyword matching for demonstration
#     return [doc for doc in documents if query.lower() in doc.lower()]

# def generate_answer(query, relevant_docs):
#     if not relevant_docs:
#         return "Sorry, I couldn't find any relevant information."
#     # Concatenate relevant docs as a simple answer
#     return "Based on my knowledge:\n" + "\n".join(relevant_docs)

# def main():
#     # Example knowledge base will use real one once the environment is set up
    
#     documents = [

#         "Not much just hanging out. Wassup with you?",
#         "Hello! How can i help you today?",
#         "RAG stands for Retrieval-Augmented Generation.",
#         "A RAG chatbot retrieves relevant documents and generates answers.",
#         "RAG combines retrieval and generative models for better responses.",
#         """RAG in the context of artificial intelligence refers to Retrieval-Augmented Generation, 
# a technique that combines large language models (LLMs) with external data retrieval to enhance accuracy and context-awareness. 
# In essence, it helps LLMs access and incorporate information beyond their pre-existing training data. """
    
#     ]
    
#     print("Welcome to the RAG Chatbot! Type 'exit' to quit.")
    
#     while True:
    
#         query = input("You: ")
    
#         if query.lower() == 'exit':
#             break
    
#         relevant_docs = get_relevant_docs(query, documents)
#         answer = generate_answer(query, relevant_docs)
    
#         print("Bot:", answer)


# if __name__ == "__main__":
#     main()


# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from upload_router import router as upload_router
from query_router import router as query_router

app = FastAPI(
    
    title="Document RAG API", 
    version="1.0.0", 
    description="API for document ingestion and retrieval-augmented generation"
    
    )

app.add_middleware(

    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],

)

app.include_router(upload_router, prefix="/api")
app.include_router(query_router, prefix="/api")
