import subprocess
import os
import time
import requests
import sys

processes = []

def start_ollama_instance(port, home_dir):
    env = os.environ.copy()
    env["OLLAMA_HOME"] = home_dir
    env["OLLAMA_HOST"] = f"127.0.0.1:{port}"

    return subprocess.Popen(
        ['ollama', 'serve'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        env=env
    )

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

def stop_server():
    print("\n🛑 Fermeture des instances Ollama...")
    for proc in processes:
        proc.terminate()

def main():
    global processes
    port_gamemaster = sys.argv[1]
    port_narrator = sys.argv[2]
    instances = [
        {"port": port_gamemaster, "home": "./ollama_instance1"},
        {"port": port_narrator, "home": "./ollama_instance2"}
    ]

    for inst in instances:
        proc = start_ollama_instance(inst["port"], inst["home"])
        if wait_for_server(inst["port"]):
            processes.append(proc)
        else:
            print(f"Échec du démarrage Ollama sur le port {inst['port']} ⛔️")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Fermeture des instances Ollama...")
        for proc in processes:
            proc.terminate()

if __name__ == "__main__":
    main()