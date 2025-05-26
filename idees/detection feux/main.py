import cv2
import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split

# Chargement des images et étiquettes
def load_images(data_dir):
    images = []
    labels = []
    label_map = {'red': 0, 'yellow': 1, 'green': 2}
    
    for label in label_map.keys():
        path = os.path.join(data_dir, label)
        for img_name in os.listdir(path):
            img_path = os.path.join(path, img_name)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (32, 32))  # Redimensionnement pour simplifier
            images.append(img)
            labels.append(label_map[label])
    
    return np.array(images) / 255.0, np.array(labels)

# Chargement des données
data_dir = "images"  # Dossier contenant les sous-dossiers red, yellow, green
X, y = load_images(data_dir)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Création du modèle
model = keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(3, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Entraînement
epochs = 100
model.fit(X_train, y_train, epochs=epochs, validation_data=(X_test, y_test))

# Fonction de prédiction
def predict_traffic_light(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Erreur : Impossible de charger l'image '{image_path}'. Vérifiez le chemin.")
    
    img = cv2.resize(img, (32, 32)) / 255.0
    img = np.expand_dims(img, axis=0)
    
    prediction = model.predict(img)[0]  # Récupérer le tableau de probas
    classes = ['red', 'yellow', 'green']
    
    max_index = np.argmax(prediction)
    confidence = prediction[max_index] * 100  # Convertir en pourcentage
    
    return classes[max_index], confidence, {classes[i]: round(prediction[i] * 100, 2) for i in range(3)}

# Exemple d'utilisation
image_path = "test_images/green_light.jpg"  # Remplacez par le chemin d'une image de test
resultat = predict_traffic_light(image_path)
print("\n===== Résultats =====")
print("Le feu est :", resultat[0])
print(f"Certitude : {resultat[1]:.3f}")
print(f"> Rouge : {resultat[2]['red']}\n> Jaune : {resultat[2]['yellow']}\n> Vert : {resultat[2]['green']}")
print("=====================\n")
