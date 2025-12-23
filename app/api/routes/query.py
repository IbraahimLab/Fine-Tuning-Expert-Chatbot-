from fastapi import APIRouter, HTTPException
from app.api.schemas import QueryRequest, QueryResponse
from app.rag.chain import answer_question

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    q = (req.question or "").strip()
    if not q:
        raise HTTPException(status_code=400, detail="Question is required.")
    return answer_question(q)
