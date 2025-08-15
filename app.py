from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from services.llm_service import get_llm_response
import time

request_counts = {}
RATE_LIMIT_PER_MINUTE = 1000

def rate_limiter(request):
    ip = request.client.host
    now = int(time.time())
    
    if ip not in request_counts:
        request_counts[ip] = []

    request_counts[ip] = [ts for ts in request_counts[ip] if now - ts < 60]

    if len(request_counts[ip]) >= RATE_LIMIT_PER_MINUTE:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    request_counts[ip].append(now)
    return True


app = FastAPI()


class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest, allowed: bool = Depends(rate_limiter)):
    """
    Receives a message, validates it, gets a response from the LLM,
    and returns the reply. Now includes input validation and rate limiting.
    """
    if not request.message or len(request.message.strip()) == 0:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    if len(request.message) > 1000: # Message length validation
        raise HTTPException(status_code=400, detail="Message is too long")
    
    if '<' in request.message or '>' in request.message:
        raise HTTPException(status_code=400, detail="Invalid characters in message")

    reply = get_llm_response(request.message)
    return {"reply": reply}