import logging
from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel, Field
from typing import Dict
from services.llm_service import get_llm_response, LLMServiceError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)

@app.post("/chat")
def chat_endpoint(request: ChatRequest) -> Dict[str, str]:
    message = request.message.strip()

    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    if '<' in message or '>' in message:
        raise HTTPException(status_code=400, detail="Invalid characters in message")

    try:
        reply = get_llm_response(message)
        return {"reply": reply}
    except LLMServiceError as e:
        logging.error(f"LLM Service Error: {e.error_type.value} - {e.message}")
        raise HTTPException(status_code=500, detail=f"LLM Error: {e.message}")
    except Exception as e:
        logging.error(f"An unexpected error occurred in chat_endpoint: {e}")
        raise HTTPException(status_code=500, detail="An unexpected internal server error occurred.")
