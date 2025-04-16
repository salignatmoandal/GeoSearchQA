# app/model/ollama_client.py
import httpx
import logging
import json
import os
import time

class OllamaClient:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
        self.model = os.getenv("MODEL_NAME", "llama3:8b")
        logging.info(f"OllamaClient initialisé avec base_url={self.base_url}, model={self.model}")

    async def generate_completion(self, prompt: str, temperature: float = 0.7, max_tokens: int = 250):
        logging.info(f"Génération de complétion pour le modèle {self.model}")
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                # URL de l'API chat
                url = f"{self.base_url}/api/chat"
                
                # Payload pour l'API
                payload = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "stream": False,
                    "max_tokens": max_tokens  # Limite la longueur de la réponse
                }
                
                logging.info(f"Envoi de requête à {url} avec modèle {self.model}")
                logging.info(f"Taille du prompt: {len(prompt)} caractères")
                
                # Envoi de la requête
                response = await client.post(url, json=payload, timeout=60.0)
                logging.info(f"Statut de la réponse: {response.status_code}")
                
                # Traitement de la réponse
                if response.status_code == 200:
                    try:
                        result = response.json()
                        content = result.get("message", {}).get("content", "")
                        if content:
                            logging.info(f"Réponse reçue, longueur: {len(content)}")
                            return {"response": content}
                        else:
                            logging.warning("Réponse vide reçue")
                    except Exception as e:
                        logging.error(f"Erreur lors du traitement de la réponse: {str(e)}")
                else:
                    error_text = response.text
                    logging.error(f"Erreur HTTP {response.status_code}: {error_text}")
                    
                    # Si le problème est avec le modèle, afficher un message clair
                    if "model not found" in error_text:
                        logging.error(f"Le modèle {self.model} n'est pas disponible dans Ollama")
                        return {"response": f"Erreur: Le modèle {self.model} n'est pas disponible. Veuillez vérifier votre installation Ollama."}
            
            # En cas d'échec, fournir une réponse par défaut
            return {"response": "Je n'ai pas pu générer une réponse avec le modèle demandé."}
                
        except httpx.TimeoutException:
            logging.error("Timeout lors de la connexion à Ollama")
            return {"response": "Le service LLM a mis trop de temps à répondre"}
        except httpx.ConnectError:
            logging.error(f"Impossible de se connecter à Ollama sur {self.base_url}")
            return {"response": "Impossible de se connecter au service LLM"}
        except Exception as e:
            logging.error(f"Erreur inattendue: {str(e)}")
            return {"response": f"Une erreur s'est produite: {str(e)}"}