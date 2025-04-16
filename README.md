# GeoSearchQA
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
│   ├── api/
│   │   └── routes.py              # 🎯 /v1/chat/completions endpoint
│   ├── context/
│   │   ├── location.py            #  GPS or IP-based location
│   │   ├── favorites.py           #  Custom favorite places
│   ├── model/
│   │   └── ollama_client.py       #  HTTP calls to Ollama (LLaMA3)
│   ├── core/
│   │   └── prompt_builder.py      #  Assembles context + question
│   ├── main.py                    #  Launches FastAPI app
│   └── config.py                  #  Loads .env + constants
├── .env                           #  API keys, local configs
├── requirements.txt               #  Python dependencies
├── Dockerfile                     #  Containerization
├── docker-compose.yml             # Multi-container setup
└── Makefile                       #  Build and deployment commands
```

# Installation 
1. Clone repository 
   `git clone https://github.com/yourusername/geosearchqa.git
   cd geosearchqa`

