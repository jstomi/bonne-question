import subprocess
import time

import requests

import variables
from instances.gamemaster import call_game_master
from instances.narrator import call_narrator
from instances.validity import call_validity

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


def new_player_prompt(player_prompt):
    print("⌛ : " + str(current_step))

    validity = call_validity(player_prompt)

    if (validity['VALID']):
        game_master_response = call_game_master(player_prompt)
        response = call_narrator(player_prompt)
    else:
        print("Ce n'est pas valide comme prompt !")
        print(player_prompt)


def main():
    server_process = subprocess.Popen(
        ['python', 'server.py', str(variables.PORTS[0]), str(variables.PORTS[1]), str(variables.PORTS[2])])

    print("⏳ Attente du démarrage des instances Ollama...")
    for port in variables.PORTS:
        if wait_for_server(port):
            print(f"Ollama prêt sur le port {port} ✅")
        else:
            print(f"⛔️ Ollama non disponible sur le port {port}")
            server_process.terminate()
            return

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
