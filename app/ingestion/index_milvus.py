from langchain_milvus import Milvus
from langchain_core.documents import Document
from app.core.config import settings
from app.core.embeddings import get_embeddings


def index_into_milvus(chunks: list[Document]) -> None:
    if not chunks:
        print("No chunks to index.")
        return

    embeddings = get_embeddings()

    # This will create the collection if it doesn't exist
    vectorstore = Milvus(
        embedding_function=embeddings,
        collection_name=settings.milvus_collection,
        connection_args={
            "uri": settings.milvus_uri,
            "token": settings.milvus_token,
        },
        # Drop if you want a clean rebuild each time:
        # drop_old=True,
    )

    vectorstore.add_documents(chunks)
    print(f"Indexed {len(chunks)} chunks into Milvus collection '{settings.milvus_collection}'.")
