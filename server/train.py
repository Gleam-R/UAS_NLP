import os
import json
import numpy as np
import tensorflow as tf
import nltk
import pickle
import re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import LabelEncoder

nltk.download("punkt")

# Load dataset
with open(r"C:\Users\Mrizky\Project\Personal Projects\UAS_NLP\server\Intents.json", encoding="utf-8") as file:
    data = json.load(file)

# Initialize tools
stemmer = PorterStemmer()
encoder = LabelEncoder()
tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=2000, filters="")

def preprocess_text(text):
    """Preprocess text by removing punctuation, tokenizing, and stemming."""
    # Remove special characters but keep numbers and spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Tokenize and apply stemming
    words = word_tokenize(text)
    words = [stemmer.stem(word) for word in words]  # Apply stemming
    return " ".join(words)

# Data processing
patterns = []
tags = []
responses = {}
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        clean_pattern = preprocess_text(pattern)
        patterns.append(clean_pattern)
        tags.append(intent["tag"])
    responses[intent["tag"]] = intent["responses"]

# Tokenization and encoding
tokenizer.fit_on_texts(patterns)
X = tokenizer.texts_to_matrix(patterns, mode="tfidf")  # Using TF-IDF

y = encoder.fit_transform(tags)
y = tf.keras.utils.to_categorical(y, num_classes=len(encoder.classes_))

# Model building
model = Sequential([
    Dense(256, input_shape=(X.shape[1],), activation="relu"),
    Dropout(0.5),
    Dense(128, activation="relu"),
    Dropout(0.3),
    Dense(64, activation="relu"),
    Dropout(0.2),
    Dense(len(encoder.classes_), activation="softmax")
])

# Compile model
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Train model
model.fit(X, y, epochs=70, batch_size=8, verbose=1)

# Save model and tokenizer
model.save("chatbot_model.h5", save_format="h5")
with open("tokenizer.pickle", "wb") as f:
    pickle.dump(tokenizer, f)
with open("encoder.pickle", "wb") as f:
    pickle.dump(encoder, f)

print("Training complete! Model and tokenizer saved.")
