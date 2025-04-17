import variables
from instances.call import call_chat_instance

narrator_history = [{"role": "system", "content": variables.NARRATOR_SYSTEM_PROMPT}]


def call_narrator(prompt):
    global narrator_history
    result = call_chat_instance(
        "📢",
        variables.PORTS[1],
        {
            "model": variables.MODEL,
            "messages": narrator_history + [{"role": "user", "content": variables.NARRATOR_PROMPT(prompt)}],
            "stream": False,
        })
    narrator_history.append({"role": "assistant", "content": str(result)})
    return result
