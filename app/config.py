import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    PROJECT_NAME: str = "AI Interview Screener"
    VERSION: str = "1.0.0"

settings = Settings()
