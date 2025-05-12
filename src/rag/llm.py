import os
from langchain_mistralai import ChatMistralAI
from .config import MISTRAL_API_KEY

os.environ["MISTRAL_API_KEY"] = MISTRAL_API_KEY

def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        temperature=0.0,
        max_retries=2,
    )
