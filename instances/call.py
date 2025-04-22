import json

import requests
from yaspin import yaspin


def call_generate_instance(name, port, payload):
    url = f"http://localhost:{port}/api/generate"
    print(name + " : \"" + payload["prompt"] + "\"")
    print(" ", end="")
    with yaspin(color="cyan") as spinner:
        response = requests.post(url, json=payload)

    if response.ok:
        spinner.ok("⬇️")
        try:
            result = json.loads(response.json()['response'])
            print("\"" + str(result) + "\"")
            print()
            return result
        except json.JSONDecodeError:
            print("Erreur : La réponse reçue n'est pas un JSON valide :", response.json()['response'])
            return None
    else:
        spinner.fail("💥")
        print("Erreur lors de l'appel API :", response.text)
        return None


def call_chat_instance(name, port, payload, type='text'):
    url = f"http://localhost:{port}/api/chat"
    print(name + " : " + str(payload["messages"][-2:]))
    with yaspin(color="cyan") as spinner:
        response = requests.post(url, json=payload)
    if response.ok:
        spinner.ok("⬇️")
        try:
            if type == 'json':
                result = json.loads(response.json()['message']['content'])
            else:
                result = response.json()['message']['content']
            print("\"" + str(result) + "\"")
            print()
            return result
        except json.JSONDecodeError:
            print("Erreur : La réponse reçue n'est pas un JSON valide :", response.json()['message']['content'])
            return None
    else:
        spinner.fail("💥")
        print("Erreur lors de l'appel API :", response.text)
        print("****************")
        print(response)
        return None
