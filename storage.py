import json
import os

def load_data(filename):
    # getting stuff out of the file: if there is no file, just return an empty list or it crashes.
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(filename, data):
    # putting stuff back in the file
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError as e:
        print(f"Error saving data to {filename}: {e}")