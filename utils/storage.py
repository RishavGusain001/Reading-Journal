### storage.py
import json
import os

def load_json(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)