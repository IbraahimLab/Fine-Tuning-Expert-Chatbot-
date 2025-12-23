import os
import httpx
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000/query")

st.title("PDF RAG (Milvus + Docling + Groq)")

question = st.text_input("Ask a question about your PDFs")

if st.button("Ask") and question.strip():
    with st.spinner("Thinking..."):
        r = httpx.post(API_URL, json={"question": question}, timeout=60)
        r.raise_for_status()
        data = r.json()

    st.subheader("Answer")
    st.write(data["answer"])

    st.subheader("Sources")
    st.json(data["sources"])
