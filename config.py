import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = "gemini-2.5-flash"
    
    MAX_CODE_LENGTH = 10000  
    CONFIDENCE_THRESHOLD = 0.7  
    
    VERBOSE = os.getenv("VERBOSE", "false").lower() == "true"
    OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT", "rich")  # rich, json, plain 