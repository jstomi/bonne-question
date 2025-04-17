import json

PORTS = [11434, 11435, 11436]  # 0: gamemaster, 1: narrator, 2:validity

MODEL = 'gemma3:12b'

with open("prompts/narrator_system_prompt.txt", "r", encoding="utf-8") as f:
    NARRATOR_SYSTEM_PROMPT = f.read()

with open("prompts/gamemaster_system_prompt.txt", "r", encoding="utf-8") as f:
    gamemaster_system_prompt_variables = ""
    with open('prompts/game_variable.json', 'r', encoding='utf-8') as f2:
        game_variables = json.load(f2)
        for game_variable in game_variables:
            gamemaster_system_prompt_variables = gamemaster_system_prompt_variables + "- " + game_variable + " : " + \
                                                 game_variables[game_variable]["description"] + ".\n"

    GAMEMASTER_SYSTEM_PROMPT = f.read().replace("#variables#", gamemaster_system_prompt_variables)

with open("prompts/validity_system_prompt.txt", "r", encoding="utf-8") as f:
    VALIDITY_SYSTEM_PROMPT = f.read()


def NARRATOR_PROMPT(prompt):
    return "player said : '" + prompt + "'.answer him."
