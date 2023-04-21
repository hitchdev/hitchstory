import json
from textblob import TextBlob


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


def add_item():
    item = input("Enter a to-do item: ")
    corrected_item = correct_spelling(item)
    if corrected_item != item:
        print(f'Did you mean "{corrected_item}"?')
        choice = input("Enter Y to confirm, or any other key to re-enter: ")
        if choice.lower() == "y":
            item = corrected_item
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

while True:
    print("To-do list:")
    for i, item in enumerate(data):
        print(f"{i + 1}. {item}")

    print("Options:")
    print("1. Add item")
    print("2. Remove item")
    print("3. Quit")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        continue

    if choice == 1:
        add_item()
    elif choice == 2:
        remove_item()
    elif choice == 3:
        break
    else:
        print("Invalid input. Please enter a valid number.")
