import requests
import json


def call_game_master(prompt, port=11434, model='gemma3:12b'):
    url = f"http://localhost:{port}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": {
            "type": "object",
            "properties": {
                "valid": {
                    "type": "boolean"
                },
                "deplacement": {
                    "type": "boolean"
                }
            },
            "required": [
                "valid",
                "deplacement"
            ]
        }
    }

    response = requests.post(url, json=payload)
    if response.ok:
        try:
            return json.loads(response.json()['response'])
        except json.JSONDecodeError:
            print("Erreur : La réponse reçue n'est pas un JSON valide :", response.json()['response'])
            return None
    else:
        print("Erreur lors de l'appel API :", response.text)
        return None