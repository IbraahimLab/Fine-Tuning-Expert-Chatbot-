from langchain_classic.chains.conversation.memory import ConversationSummaryMemory
from app.core.llm import get_llm

# Module-level singleton memory (persists per process)
_memory = None


def get_conversation_memory():
    """
    Returns a singleton ConversationSummaryMemory instance.

    - Summarises older conversation turns
    - Keeps recent turns verbatim
    - Uses the same LLM as the main chain
    """
    global _memory

    if _memory is None:
        _memory = ConversationSummaryMemory(
            llm=get_llm(),
            memory_key="chat_history",
            return_messages=True,
        )

    return _memory
