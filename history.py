import json
import os
from datetime import datetime

HISTORY_DIR = "history_data"

def load_history(user):
    path = os.path.join(HISTORY_DIR, f"{user}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def add_to_history(user, feature, input_text, response_text):
    os.makedirs(HISTORY_DIR, exist_ok=True)
    path = os.path.join(HISTORY_DIR, f"{user}.json")
    history = load_history(user)
    history.append({
        "feature": feature,
        "input": input_text,
        "response": response_text,
        "time": datetime.now().strftime("%d-%b %H:%M")
    })
    with open(path, "w") as f:
        json.dump(history, f, indent=2)

def clear_history(user):
    path = os.path.join(HISTORY_DIR, f"{user}.json")
    if os.path.exists(path):
        os.remove(path)
