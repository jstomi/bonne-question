import json

import variables
from instances.call import call_chat_instance

gamemaster_history = [{"role": "system", "content": variables.GAMEMASTER_SYSTEM_PROMPT}]


def call_game_master(prompt):
    global gamemaster_history
    with open('prompts/game_variable.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    payload = {
        "model": variables.MODEL,
        "messages": gamemaster_history + [{"role": "user", "content": prompt}],
        "stream": False,
        "format": {
            "type": "object",
            "properties": {
                cle: {"type": "boolean"} for cle in data.keys()
            }
        }
    }
    result = call_chat_instance("🎲", variables.PORTS[0], payload, "json")
    gamemaster_history.append({"role": "assistant", "content": str(result)})
    return result
