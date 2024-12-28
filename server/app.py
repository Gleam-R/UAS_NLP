from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import pickle
import numpy as np
import json
import random

# Enable CORS
app = Flask(__name__)
CORS(app)  # This will allow all domains to access this server

# Load model and preprocessing tools
model = tf.keras.models.load_model(r"C:\Users\Mrizky\Project\Personal Projects\UAS_NLP\chatbot_model.h5")

# Load tokenizer and encoder
with open(r"C:\Users\Mrizky\Project\Personal Projects\UAS_NLP\tokenizer.pickle", "rb") as f:
    tokenizer = pickle.load(f)
with open(r"C:\Users\Mrizky\Project\Personal Projects\UAS_NLP\encoder.pickle", "rb") as f:
    encoder = pickle.load(f)

# Load intents.json
with open(r"C:\Users\Mrizky\Project\Personal Projects\UAS_NLP\server\Intents.json") as file:
    intents = json.load(file)

# Preprocessing function for input text
def preprocess_input(input_text):
    # Preprocess input text: e.g., convert to lowercase
    return input_text.lower()

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        question = data.get("question", "")

        if not question:
            return jsonify({"response": "Maaf, saya tidak mengerti pertanyaan Anda."})

        # Preprocessing question
        corrected_question = preprocess_input(question)
        tokens = tokenizer.texts_to_matrix([corrected_question], mode="binary")

        # Predict tag
        prediction = model.predict(tokens)
        tag = encoder.inverse_transform([np.argmax(prediction)])[0]

        # Find response from intents.json
        for intent in intents["intents"]:
            if intent["tag"] == tag:
                response = random.choice(intent["responses"])
                return jsonify({
                    "response": response,
                    "corrected_input": corrected_question
                })

        return jsonify({
            "response": "Maaf, saya tidak mengerti pertanyaan Anda.",
            "corrected_input": corrected_question
        })

    except Exception as e:
        return jsonify({"response": f"Terjadi kesalahan: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
