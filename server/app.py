from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import pickle
import numpy as np
import json
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re

# Download necessary NLTK data
nltk.download('punkt')

app = Flask(__name__)
CORS(app)  # Allow all domains to access this server

# Load model and preprocessing tools
MODEL_PATH = r"C:\Users\Mrizky\Project\Personal Projects\UAS_NLP\chatbot_model.h5"
TOKENIZER_PATH = r"C:\Users\Mrizky\Project\Personal Projects\UAS_NLP\tokenizer.pickle"
ENCODER_PATH = r"C:\Users\Mrizky\Project\Personal Projects\UAS_NLP\encoder.pickle"
INTENTS_PATH = r"C:\Users\Mrizky\Project\Personal Projects\UAS_NLP\server\Intents.json"

intents = None
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    with open(TOKENIZER_PATH, "rb") as f:
        tokenizer = pickle.load(f)
    with open(ENCODER_PATH, "rb") as f:
        encoder = pickle.load(f)
    with open(INTENTS_PATH, "r", encoding="utf-8") as file:
        intents = json.load(file)
except Exception as e:
    print(f"Error loading model or files: {e}")

# Initialize tools
stemmer = PorterStemmer()

# Dictionary of correct words (you can expand this)
word_dict = ["skripsi", "tugas akhir", "Jangan", "chatbot", "kuliah", "Kerja Praktek", "Kelas"]

def levenshtein(a, b):
    """Calculate Levenshtein Distance between two words."""
    if len(a) < len(b):
        return levenshtein(b, a)
    
    if len(b) == 0:
        return len(a)
    
    a = list(a)
    b = list(b)
    
    # Create a matrix to store distances
    distance = range(len(b) + 1)
    
    for i, ca in enumerate(a):
        distance_ = [i + 1]
        for j, cb in enumerate(b):
            cost = 0 if ca == cb else 1
            distance_.append(min((distance[j + 1] + 1), (distance_[j] + 1), (distance[j] + cost)))
        distance = distance_
    
    return distance[-1]

def correct_spelling(word):
    """Correct a word by finding the closest match from the dictionary using Levenshtein Distance."""
    closest_match = min(word_dict, key=lambda x: levenshtein(word, x))
    return closest_match if levenshtein(word, closest_match) < 3 else word  # Return original if no close match found

def preprocess_text(text):
    """Preprocess text by removing punctuation, correcting spelling, tokenizing, and stemming."""
    # Remove special characters but keep numbers and spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove any non-alphanumeric characters

    # Tokenize text, apply autocorrection, and apply stemming
    words = word_tokenize(text)
    corrected_words = [correct_spelling(word) for word in words]  # Apply spelling correction
    words = [stemmer.stem(word) for word in corrected_words]  # Apply stemming
    return " ".join(words)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"response": "Maaf, saya tidak mengerti pertanyaan Anda."})

        # Preprocessing question
        corrected_question = preprocess_text(question)
        tokens = tokenizer.texts_to_matrix([corrected_question], mode="tfidf")

        # Predict tag
        prediction = model.predict(tokens)
        tag = encoder.inverse_transform([np.argmax(prediction)])[0]

        # Ensure intents are loaded
        if not intents:
            return jsonify({"response": "Error: Intents file not loaded."})

        # Find response from intents.json
        for intent in intents["intents"]:
            if intent["tag"] == tag:
                response = random.choice(intent["responses"])
                return jsonify({
                    "response": response,
                    "corrected_input": corrected_question  # Only return corrected text as string
                })

        return jsonify({
            "response": "Maaf, saya tidak mengerti pertanyaan Anda.",
            "corrected_input": corrected_question  # Only return corrected text as string
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": f"Terjadi kesalahan: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
