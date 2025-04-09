import requests
import json

def call_narrator(prompt, port=11435, model='gemma3:12b'):
    url = f"http://localhost:{port}/api/generate"
    payload = {
        "model": model,
        "prompt": "player said : '" + prompt + "'.answer him.",
        "stream": False,
    }

    response = requests.post(url, json=payload)
    if response.ok:
        try:
            return response.json()['response']
        except json.JSONDecodeError:
            print("Erreur : La réponse reçue n'est pas un JSON valide :", response.json())
        return None
    else:
        print("Erreur lors de l'appel API :", response.text)
        return None