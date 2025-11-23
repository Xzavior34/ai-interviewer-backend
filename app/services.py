import os
import json
import asyncio
from openai import AsyncOpenAI
from app.models import EvaluationResponse

# Initialize Async Client (Non-blocking)
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an expert Technical Recruiter. 
Evaluate the candidate's answer based on clarity, technical accuracy, and depth.
You MUST return a JSON object with these exact keys:
- score (integer 1-5)
- summary (one sentence)
- improvement (one constructive suggestion)
"""

async def evaluate_text(text: str) -> EvaluationResponse:
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo-0125", # fast and cheap model
            response_format={"type": "json_object"}, # CRITICAL: Enforces valid JSON
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Candidate says: {text}"}
            ],
            temperature=0.2 # Low temperature for consistent scoring
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)
        
        return EvaluationResponse(**data)
        
    except Exception as e:
        # In production, log this error properly
        print(f"LLM Error: {e}")
        # Fallback response so the API doesn't crash
        return EvaluationResponse(score=1, summary="Error processing answer", improvement="Retry submission")

async def rank_candidates_concurrently(candidates):
    # Create a list of async tasks
    tasks = []
    for cand in candidates:
        tasks.append(process_candidate(cand))
    
    # Run all evaluations in PARALLEL (Fast!)
    results = await asyncio.gather(*tasks)
    
    # Sort by score descending
    return sorted(results, key=lambda x: x['score'], reverse=True)

async def process_candidate(candidate):
    # Helper to link ID with result
    eval_result = await evaluate_text(candidate.answer)
    return {
        "id": candidate.candidate_id,
        "answer": candidate.answer,
        "score": eval_result.score,
        "summary": eval_result.summary,
        "improvement": eval_result.improvement
    }
