# GeoSearchQA - Model Context Protocol 
A context-aware AI assistant that leverages geolocation data and local information to provide relevant answers to user queries.

# Overview

GeoSearchQA enhances Large Language Models with geographic context awareness. It uses location data to tailor responses to users, making it ideal for travel recommendations, local business inquiries, and location-specific questions.
Key features:
Location-aware responses using GPS or IP-based geolocation
Integration with Llama models via Ollama
Context building with local search results
Docker-based deployment for easy setup

# Architecture 
```
geo-mcp-llama/
├── app/
│   ├── api/                    # API endpoints
│   │   └── routes.py           # /api/v1/chat/completions
│   ├── context/                # Location + user context
│   │   ├── location.py         # GPS/IP-based geolocation logic
│   │   └── favorites.py        # User-defined favorite places
│   ├── core/                   # Prompt building logic
│   │   └── prompt_builder.py   # Constructs prompts with context
│   ├── model/                  # Ollama client interface
│   │   └── ollama_client.py    # Calls to Ollama API
│   ├── config.py               # .env loader and app constants
│   └── main.py                 # FastAPI app launcher
├── .env                        # Environment variables
├── Dockerfile                  # App container
├── docker-compose.yml          # Multi-container (API + Ollama)
├── Makefile                    # Build and run automation
└── requirements.txt            # Python dependencies
```

# Quick Start 
 **Prequisites**
- Docker & Docker Compose
# Installation 
```
git clone https://github.com/yourusername/geosearchqa.git
cd geosearchqa

cp .env.example .env  # Then edit .env with your API keys
```

# Build & Run 
Use the included `Makefile` for convenience:
```
make docker-build     # Build the API and Ollama containers
make docker-run       # Run both containers
```
**Then pull the model inside the Ollama container:**
```
docker exec -it geosearchqa-ollama-1 sh
ollama pull llama3:8b
exit
```

Or use another model, such as mistral:7b, by updating .env:
```
MODEL_NAME=mistral:7b
```

# API Usage
_The main API endpoint is_
```
POST /api/v1/chat/completions
```

# Sample curl Request
```
curl -X POST http://localhost:8000/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What are the best wine bars in Montmartre that serve orange wine and are open on Monday night?"}
    ],
    "max_tokens": 150
  }'

```


