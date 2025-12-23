from langchain_docling import DoclingLoader
from langchain_core.documents import Document


def parse_pdfs_with_docling(pdf_paths: list[str]) -> list[Document]:
    docs: list[Document] = []
    for path in pdf_paths:
        loader = DoclingLoader(file_path=path)
        docs.extend(loader.load())
    return docs
