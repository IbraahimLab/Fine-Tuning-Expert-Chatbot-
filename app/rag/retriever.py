from langchain_milvus import Milvus
from app.core.config import settings
from app.core.embeddings import get_embeddings


def get_vectorstore():
    embeddings = get_embeddings()
    return Milvus(
        embedding_function=embeddings,
        collection_name=settings.milvus_collection,
        connection_args={
            "uri": settings.milvus_uri,
            "token": settings.milvus_token,
        },
    )


def get_retriever():
    vs = get_vectorstore()
    return vs.as_retriever(search_kwargs={"k": settings.top_k})
