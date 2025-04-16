import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys et configurations
    BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    MODEL_NAME = os.getenv("MODEL_NAME", "llama2")
    
    # Paramètres de recherche
    MAX_SEARCH_RESULTS = 5
    MAX_CONTEXT_LENGTH = 2048
    
    # Configuration de l'API
    API_VERSION = "v1"
    DEFAULT_TEMPERATURE = 0.7

