# Placeholder for the LLM API call function
import requests

def ask_ollama(prompt, model='llama3'):
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': model,
            'prompt': prompt,
            'stream': False
        }
    )
    response.raise_for_status()  # Optional: raise error if request failed
    return response.json()['response']