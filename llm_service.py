import os
import logging
from enum import Enum
import google.generativeai as genai
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

class LLMServiceError(Exception):
    def __init__(self, error_type, message):
        self.error_type = error_type
        self.message = message
        super().__init__(self.message)

class LLMErrorType(Enum):
    AUTHENTICATION = "AUTHENTICATION_ERROR"
    RATE_LIMIT = "RATE_LIMIT_ERROR"
    NOT_FOUND = "NOT_FOUND_ERROR"
    CONNECTION = "CONNECTION_ERROR"
    UNKNOWN = "UNKNOWN_ERROR"

try:
    genai.configure(api_key=os.getenv("API_KEY"))
except Exception as e:
    logging.error("Failed to configure Gemini API. Check API key.")
    raise LLMServiceError(LLMErrorType.AUTHENTICATION, "Gemini API key is not configured or is invalid.")

def get_llm_response(prompt: str) -> str:
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Gemini API call failed: {e}")
        raise LLMServiceError(LLMErrorType.UNKNOWN, "The LLM service failed to generate a response.")