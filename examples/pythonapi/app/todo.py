import json
from textblob import TextBlob


class Misspelling(Exception):
    pass


def load_data():
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    return data


def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)


def list_items():
    for item in load_data():
        print(item)
    return


def add_item(item):
    corrected_item = correct_spelling(item)
    if corrected_item != item:
        raise Misspelling(f'Did you mean "{corrected_item}"?')
    print(f"To do added {item}")
    data.append(item)
    save_data(data)


def remove_item():
    print("Current to-do list:")
    for i, item in enumerate(data):
        print(f"{i + 1}. {item}")
    try:
        index = int(input("Enter the number of the item to remove: "))
        data.pop(index - 1)
        save_data(data)
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid number.")


def correct_spelling(text):
    blob = TextBlob(text)
    corrected = str(blob.correct())
    if corrected != text:
        return suggest_spelling(text)
    else:
        return corrected


def suggest_spelling(text):
    blob = TextBlob(text)
    suggestion = str(blob.correct())
    return suggestion


data = load_data()
