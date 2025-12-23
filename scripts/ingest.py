from app.ingestion.load_pdfs import list_pdf_paths
from app.ingestion.parse_docling import parse_pdfs_with_docling
from app.ingestion.chunking import chunk_documents
from app.ingestion.index_milvus import index_into_milvus


def main():
    pdf_paths = list_pdf_paths()
    if not pdf_paths:
        print("No PDFs found in data/pdfs. Add PDFs and run again.")
        return

    docs = parse_pdfs_with_docling(pdf_paths)
    chunks = chunk_documents(docs)
    index_into_milvus(chunks)


if __name__ == "__main__":
    main()
