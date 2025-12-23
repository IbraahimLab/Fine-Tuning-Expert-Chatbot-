from langchain_openai import ChatOpenAI
from app.core.config import settings


def get_llm():
    # Groq is OpenAI-compatible: base_url + api_key
    return ChatOpenAI(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        base_url=settings.groq_base_url,
        temperature=0.2,
    )
