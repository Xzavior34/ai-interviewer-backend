from pydantic import BaseModel, Field
from typing import List, Optional

# The structure required by the challenge
class EvaluationResponse(BaseModel):
    score: int = Field(..., ge=1, le=5, description="Score between 1 and 5")
    summary: str
    improvement: str

class CandidateAnswer(BaseModel):
    candidate_id: str = Field(..., description="Unique ID for the candidate")
    answer: str

class RankRequest(BaseModel):
    candidates: List[CandidateAnswer]

class RankResponse(BaseModel):
    ranked_candidates: List[dict]
