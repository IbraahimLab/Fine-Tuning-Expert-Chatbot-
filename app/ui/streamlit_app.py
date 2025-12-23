# import os
# import httpx
# import streamlit as st

# API_URL = os.environ.get("API_URL", "http://localhost:8000/query")

# st.title("PDF RAG (Milvus + Docling + Groq)")

# question = st.text_input("Ask a question about your PDFs")

# if st.button("Ask") and question.strip():
#     with st.spinner("Thinking..."):
#         r = httpx.post(API_URL, json={"question": question}, timeout=60)
#         r.raise_for_status()
#         data = r.json()

#     st.subheader("Answer")
#     st.write(data["answer"])

#     # st.subheader("Sources")
#     # st.json(data["sources"])

import os
import httpx
import streamlit as st

# -----------------------------
# Page config (must be first)
# -----------------------------
st.set_page_config(
    page_title="RAG Chat",
    page_icon="🧠",
    layout="wide",
)

API_URL = os.environ.get("API_URL", "http://localhost:8000/query")

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("## 🧠 PDF RAG Assistant")
    st.markdown(
        """
        **Tech stack**
        - Milvus (Vector DB)
        - Docling (PDF parsing)
        - LangChain + LangGraph
        - Groq (Kimi K2)

        ---
        This assistant answers questions
        **only from your PDFs**.
        """
    )

    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []

# -----------------------------
# Main title
# -----------------------------
st.markdown(
    """
    <h1 style="margin-bottom: 0.2em;">📄 Conversational PDF RAG</h1>
    <p style="color: #666; margin-top: 0;">
        Ask questions about your documents. The assistant remembers the conversation.
    </p>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Session state for UI messages
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Chat history rendering
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# User input
# -----------------------------
prompt = st.chat_input("Ask something about your PDFs...")

if prompt and prompt.strip():
    # Show user message immediately
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                r = httpx.post(
                    API_URL,
                    json={"question": prompt},
                    timeout=120,
                )
                r.raise_for_status()
                answer = r.json()["answer"]
            except Exception as e:
                answer = f"❌ Error: {e}"

        st.markdown(answer)

    # Save assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
