import os
from dotenv import load_dotenv

load_dotenv()  # loads .env in project root

def get_env(key: str) -> str:
    v = os.getenv(key)
    if not v:
        raise RuntimeError(f"Missing env var {key}")
    return v

CSV_PATH         = get_env("CSV_PATH")
PINECONE_API_KEY = get_env("PINECONE_API_KEY")
PINECONE_ENV     = get_env("PINECONE_ENVIRONMENT")
PINECONE_INDEX   = get_env("PINECONE_INDEX")
MISTRAL_API_KEY  = get_env("MISTRAL_API_KEY")
API_URL          = os.getenv("API_URL", "http://127.0.0.1:8000")
