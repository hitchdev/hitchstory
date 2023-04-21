from flask import Flask, request, jsonify, send_from_directory
from textblob import TextBlob
import json

app = Flask(__name__)


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


@app.route("/todo", methods=["GET"])
def get_todo():
    data = load_data()
    return jsonify(data)


@app.route("/todo", methods=["POST"])
def add_todo():
    data = load_data()
    item = request.json["item"]
    corrected_item = correct_spelling(item)
    if corrected_item != item:
        return jsonify({"message": corrected_item}), 400
    data.append(item)
    save_data(data)
    return jsonify({"message": "Item added successfully"}), 201


@app.route("/todo/<int:index>", methods=["DELETE"])
def delete_todo(index):
    data = load_data()
    try:
        data.pop(index - 1)
        save_data(data)
        return jsonify({"message": "Item removed successfully"}), 200
    except IndexError:
        return jsonify({"message": "Item not found"}), 404


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/styles.css")
def styles():
    return send_from_directory(".", "styles.css")


@app.route("/script.js")
def script():
    return send_from_directory(".", "script.js")


if __name__ == "__main__":
    app.run(debug=True)
