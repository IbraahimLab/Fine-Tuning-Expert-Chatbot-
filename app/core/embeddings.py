from langchain_community.embeddings import HuggingFaceEmbeddings
from app.core.config import settings


def get_embeddings():
    # Local embeddings (no API key needed)
    return HuggingFaceEmbeddings(model_name=settings.embedding_model)
