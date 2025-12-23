from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Groq (OpenAI compatible)
    groq_api_key: str = Field(..., alias="GROQ_API_KEY")
    groq_base_url: str = Field("https://api.groq.com/openai/v1", alias="GROQ_BASE_URL")
    groq_model: str = Field("moonshotai/kimi-k2-instruct-0905", alias="GROQ_MODEL")

    # Embeddings
    embedding_model: str = Field("sentence-transformers/all-MiniLM-L6-v2", alias="EMBEDDING_MODEL")

    # Milvus
    milvus_uri: str = Field(..., alias="MILVUS_URI")
    milvus_token: str = Field(..., alias="MILVUS_TOKEN")
    milvus_collection: str = Field("pdf_rag_chunks", alias="MILVUS_COLLECTION")

    # Data
    pdf_dir: str = Field("./data/pdfs", alias="PDF_DIR")

    # RAG
    top_k: int = Field(4, alias="TOP_K")


settings = Settings()
