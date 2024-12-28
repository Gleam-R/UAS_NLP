import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import LabelEncoder
from nltk.tokenize import word_tokenize
import nltk

# Load dataset
with open(r"C:\Users\Mrizky\Project\Personal Projects\UAS_NLP\server\Intents.json") as file:
    data = json.load(file)

# Preprocessing
patterns = []
tags = []
responses = {}
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        patterns.append(pattern)
        tags.append(intent["tag"])
    responses[intent["tag"]] = intent["responses"]

# Tokenization and encoding
tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=1000)
tokenizer.fit_on_texts(patterns)
X = tokenizer.texts_to_matrix(patterns, mode="binary")

encoder = LabelEncoder()
y = encoder.fit_transform(tags)
y = tf.keras.utils.to_categorical(y, num_classes=len(encoder.classes_))

# Building the model
model = Sequential([
    Dense(128, input_shape=(X.shape[1],), activation="relu"),
    Dropout(0.5),
    Dense(64, activation="relu"),
    Dropout(0.5),
    Dense(len(encoder.classes_), activation="softmax")
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.fit(X, y, epochs=200, batch_size=8, verbose=1)

# Save the model
model.save("chatbot_model.h5")
with open("tokenizer.pickle", "wb") as f:
    import pickle
    pickle.dump(tokenizer, f)
with open("encoder.pickle", "wb") as f:
    pickle.dump(encoder, f)
