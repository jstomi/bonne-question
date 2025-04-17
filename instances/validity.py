import variables
from instances.call import call_chat_instance

validity_history = [{"role": "system", "content": variables.VALIDITY_SYSTEM_PROMPT}]


def call_validity(prompt):
    global validity_history
    payload = {
        "model": variables.MODEL,
        "messages": validity_history + [{"role": "user", "content": prompt}],
        "stream": False,
        "format": {
            "type": "object",
            "properties": {
                "VALID": {"type": "boolean"},
                "JUSTIFICATION": {"type": "string"}
            },
            "required": ["VALID", "JUSTIFICATION"]
        }
    }
    result = call_chat_instance("✔️", variables.PORTS[2], payload, "json")
    validity_history.append({"role": "assistant", "content": str(result)})
    return result
