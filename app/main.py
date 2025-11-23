from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services import evaluate_text, rank_candidates_concurrently
from app.models import EvaluationResponse, RankRequest, RankResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Interview Screener",
    description="A high-performance async API for evaluating candidates.",
    version="1.0.0"
)

class SingleEvalRequest(BaseModel):
    answer: str

@app.post("/evaluate-answer", response_model=EvaluationResponse)
async def evaluate_endpoint(request: SingleEvalRequest):
    """
    Evaluates a single answer using an LLM.
    """
    if not request.answer.strip():
        raise HTTPException(status_code=400, detail="Answer cannot be empty")
    
    return await evaluate_text(request.answer)

@app.post("/rank-candidates", response_model=RankResponse)
async def rank_endpoint(request: RankRequest):
    """
    Accepts a list of candidates, evaluates them in parallel, 
    and returns them sorted by score (Highest to Lowest).
    """
    if not request.candidates:
        raise HTTPException(status_code=400, detail="List cannot be empty")
    
    ranked_results = await rank_candidates_concurrently(request.candidates)
    return RankResponse(ranked_candidates=ranked_results)

# Health check (Standard practice)
@app.get("/health")
def health_check():
    return {"status": "active"}
