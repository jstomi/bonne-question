import subprocess
import time

import requests

import variables
from instances.gamemaster import call_game_master
from instances.narrator import call_narrator
from server import stop_server

current_step = 1


def wait_for_server(port, timeout=20):
    url = f"http://localhost:{port}"
    for _ in range(timeout):
        try:
            if requests.get(url).ok:
                return True
        except requests.ConnectionError:
            pass
        time.sleep(1)
    return False


def init_ollama_instance(port, model, prompt, system_prompt=None):
    url = f"http://localhost:{port}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    if system_prompt:
        payload["system"] = system_prompt

    print(f"🟢 Initialisation de l'instance Ollama sur le port {port} ...")
    response = requests.post(url, json=payload)
    if response.ok:
        print(f"🟢 Instance Ollama sur le port {port} initialisée :")
        print("******************")
        print(response.json()['response'])
        print("******************")
    else:
        print(f"🔴 Erreur sur l'instance {port} : {response.text}")


def new_player_prompt(player_prompt):
    print("⌛ : " + str(current_step))

    game_master_response = call_game_master(player_prompt)
    print('🎲 : ' + str(game_master_response))

    if (game_master_response['valid']):
        response = call_narrator(player_prompt)
        print('📢 : ' + str(response))
    else:
        print("Ce n'est pas valide comme prompt !")
        print(player_prompt)


def main():
    server_process = subprocess.Popen(['python', 'server.py', str(variables.PORTS[0]), str(variables.PORTS[1])])

    print("⏳ Attente du démarrage des instances Ollama...")
    for port in variables.PORTS:
        if wait_for_server(port):
            print(f"Ollama prêt sur le port {port} ✅")
        else:
            print(f"⛔️ Ollama non disponible sur le port {port}")
            server_process.terminate()
            return

    init_ollama_instance(
        port=variables.PORTS[0],
        model=variables.MODEL,
        prompt=variables.GAMEMASTER_FIRST_PROMPT,
        system_prompt=variables.GAMEMASTER_SYSTEM_PROMPT
    )

    init_ollama_instance(
        port=variables.PORTS[1],
        model=variables.MODEL,
        prompt=variables.NARRATOR_FIRST_PROMPT,
        system_prompt=variables.NARRATOR_SYSTEM_PROMPT
    )
    try:
        while True:
            global current_step
            prompt = input("next action ? => ")
            new_player_prompt(prompt)
            current_step = current_step + 1
    except KeyboardInterrupt:
        print("Fermeture du jeu...")


if __name__ == "__main__":
    main()
