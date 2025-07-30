import os

# import google.generativeai as genai
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Qdrant

from infrastructure.appointment_repository import \
    LangChainAppointmentRepository


class ServiceFactory:
    """
    Crea instancias de servicios (embeddings, vectorstore, LLM, repositorios).
    """

    @staticmethod
    def get_embedding_model():
        # Modelo local sin coste de API
        return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    @staticmethod
    def get_vectorstore(embeddings):
        # Inicializa Qdrant con el embeder
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        collection = os.getenv("QDRANT_COLLECTION", "citas")
        return Qdrant(
            url=qdrant_url,
            prefer_grpc=True,
            collection_name=collection,
            embeddings=embeddings
        )

    @staticmethod
    def get_llm():
        # Configura Gemini (Google Generative AI)
        # genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        # # Usa el modelo "chat-bison-001" o similar gratuito
        # return genai.ChatModel(model="chat-bison-001")
        return True

    @staticmethod
    def get_repository():
        embeddings = ServiceFactory.get_embedding_model()
        vectorstore = ServiceFactory.get_vectorstore(embeddings)
        # Repo que usa LangChain internamente
        return LangChainAppointmentRepository(vectorstore)


# import json
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# payload = {
#     "contents": [{"parts": [{"text": prompt}]}],
# }
# response = requests.post(url, json=payload)
# content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
# print(content)