from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.llm import get_llm
from app.rag.retriever import get_retriever


PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a careful assistant. Use ONLY the provided context. If missing, say you don't know."),
        ("human", "Question: {question}\n\nContext:\n{context}"),
    ]
)


def format_docs(docs):
    # Keep it simple: include page/source metadata when available
    lines = []
    for d in docs:
        src = d.metadata.get("source") or d.metadata.get("file_path") or "unknown"
        page = d.metadata.get("page") or d.metadata.get("page_number")
        prefix = f"[source={src}" + (f", page={page}]" if page else "]")
        lines.append(f"{prefix}\n{d.page_content}")
    return "\n\n---\n\n".join(lines)


def answer_question(question: str) -> dict:
    retriever = get_retriever()
    llm = get_llm()

    docs = retriever.invoke(question)
    context = format_docs(docs)

    chain = PROMPT | llm | StrOutputParser()
    answer = chain.invoke({"question": question, "context": context})

    return {
        "answer": answer,
        "sources": [d.metadata for d in docs],
    }
