from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.llm import get_llm
from app.rag.retriever import get_retriever
from app.rag.memory import get_conversation_memory


PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a careful LLM fine-tuning expert assistant. "
            "Use ONLY the provided context. If missing, say you don't know. "
            "Explain concepts in an easy way.\n\n"
            "Conversation so far:\n{chat_history}"
        ),
        ("human", "Question: {question}\n\nContext:\n{context}"),
    ]
)


def format_docs(docs):
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
    memory = get_conversation_memory()

    # Load existing conversation summary + recent turns
    memory_vars = memory.load_memory_variables({})
    chat_history = memory_vars.get("chat_history", "")

    # Retrieve document context
    docs = retriever.invoke(question)
    context = format_docs(docs)

    # Build chain
    chain = PROMPT | llm | StrOutputParser()

    answer = chain.invoke(
        {
            "question": question,
            "context": context,
            "chat_history": chat_history,
        }
    )

    # IMPORTANT: update memory AFTER the answer
    memory.save_context(
        {"input": question},
        {"output": answer},
    )

    return {
        "answer": answer,
    }



