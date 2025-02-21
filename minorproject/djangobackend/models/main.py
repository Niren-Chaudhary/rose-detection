import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

# Paths to the dataset
rose_path = r'C:\Users\Dell\Desktop\opencv\dataset\rose_vs_notrose\rose/'
notrose_path = r'C:\Users\Dell\Desktop\opencv\dataset\rose_vs_notrose\notrose/'
healthy_path = r'C:\Users\Dell\Desktop\opencv\dataset\disease_classification\Fresh Leaf/'
black_spot_path = r'C:\Users\Dell\Desktop\opencv\dataset\disease_classification\Black Spot/'
mildew_path = r'C:\Users\Dell\Desktop\opencv\dataset\disease_classification\Downy Mildew/'

# Image size
img_size = 128

# Function to enhance image quality
def enhance_image(img):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # Sharpening filter
    img = cv2.filter2D(img, -1, kernel)
    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)  # Optional denoising
    return img

# Function to load and preprocess images for rose vs not rose
def load_images(class1_path, class2_path, img_size):
    X, y = [], []

    # Load images from class1 (e.g., roses)
    for img_name in os.listdir(class1_path):
        img_path = os.path.join(class1_path, img_name)
        img = cv2.imread(img_path)
        if img is not None:
            img = cv2.resize(img, (img_size, img_size))
            X.append(img)
            y.append(1)  # Label for class1

    # Load images from class2 (e.g., not roses)
    for img_name in os.listdir(class2_path):
        img_path = os.path.join(class2_path, img_name)
        img = cv2.imread(img_path)
        if img is not None:
            img = cv2.resize(img, (img_size, img_size))
            X.append(img)
            y.append(0)  # Label for class2

    X = np.array(X) / 255.0  # Normalize images
    y = np.array(y)
    return X, y

# Function to load disease classification images
def load_disease_images(healthy_path, black_spot_path, mildew_path, img_size):
    X, y = [], []

    # Healthy class
    for img_name in os.listdir(healthy_path):
        img_path = os.path.join(healthy_path, img_name)
        img = cv2.imread(img_path)
        if img is not None:
            img = cv2.resize(img, (img_size, img_size))
            X.append(img)
            y.append(0)  # Label for healthy

    # Black Spot class
    for img_name in os.listdir(black_spot_path):
        img_path = os.path.join(black_spot_path, img_name)
        img = cv2.imread(img_path)
        if img is not None:
            img = cv2.resize(img, (img_size, img_size))
            X.append(img)
            y.append(1)  # Label for black spot

    # Mildew class
    for img_name in os.listdir(mildew_path):
        img_path = os.path.join(mildew_path, img_name)
        img = cv2.imread(img_path)
        if img is not None:
            img = cv2.resize(img, (img_size, img_size))
            X.append(img)
            y.append(2)  # Label for mildew

    X = np.array(X) / 255.0  # Normalize images
    y = np.array(y)
    return X, y

# Data Augmentation
datagen = ImageDataGenerator(
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Load and preprocess data for rose vs not rose
X, y = load_images(rose_path, notrose_path, img_size)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
datagen.fit(X_train)

# Transfer Learning: Fine-Tuning with MobileNetV2
def create_fine_tuned_model(img_size, num_classes):
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(img_size, img_size, 3))
    base_model.trainable = False  # Freeze base model layers during initial training

    # Add custom layers for the classification task
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.5)(x)  # Add dropout for regularization
    x = Dense(128, activation='relu')(x)
    predictions = Dense(num_classes, activation='softmax' if num_classes > 2 else 'sigmoid')(x)

    # Create the final model
    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy' if num_classes > 2 else 'binary_crossentropy',
        metrics=['accuracy']
    )
    return model

# Fine-tuned model for Rose vs Not Rose
rose_model = create_fine_tuned_model(img_size, 1)
rose_model.fit(datagen.flow(X_train, y_train, batch_size=32), epochs=10, validation_data=(X_test, y_test))

# Fine-tuned model for Disease Classification
X_disease, y_disease = load_disease_images(healthy_path, black_spot_path, mildew_path, img_size)
X_train_disease, X_test_disease, y_train_disease, y_test_disease = train_test_split(X_disease, y_disease, test_size=0.2, random_state=42)
datagen.fit(X_train_disease)
disease_model = create_fine_tuned_model(img_size, 3)
disease_model.fit(datagen.flow(X_train_disease, y_train_disease, batch_size=32), epochs=10, validation_data=(X_test_disease, y_test_disease))

# Save the models
rose_model.save('fine_tuned_rose_model.keras')
disease_model.save('fine_tuned_disease_model.keras')

# Prediction Functions
def predict_disease(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Unable to load image from path {image_path}")
        return
    img = cv2.resize(img, (img_size, img_size))
    img = enhance_image(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    prediction = disease_model.predict(img)
    class_idx = np.argmax(prediction)
    labels = ['Healthy Rose', 'Black Spot', 'Mildew']
    print(f"Prediction: {labels[class_idx]}")
    plt.imshow(cv2.cvtColor(np.uint8(img[0] * 255), cv2.COLOR_BGR2RGB))
    plt.title(f"Prediction: {labels[class_idx]}")
    plt.show(block=True)

# Modified prediction function for rose and disease prediction
def predict_rose_and_disease(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Unable to load image from path {image_path}")
        return
    img = cv2.resize(img, (img_size, img_size))
    img = enhance_image(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    # First predict if it's a rose or not
    rose_prediction = rose_model.predict(img)
    if rose_prediction[0] > 0.5:
        print("It's a Rose!")
        # If it's a Rose, proceed to disease classification
        predict_disease(image_path)
    else:
        print("It's Not a Rose!")
        print("No disease prediction is made for non-rose images.")
    
    # Show the image with its rose prediction
    plt.imshow(cv2.cvtColor(np.uint8(img[0] * 255), cv2.COLOR_BGR2RGB))
    plt.title(f"Prediction: {'Rose' if rose_prediction[0] > 0.7 else 'Not Rose'}")
    plt.show(block=True)

# Example usage
#predict_rose_and_disease(r'C:\Users\Dell\Desktop\minorproject\minorproject\djangobackend\models\sample\grapes.jpg')
predict_rose_and_disease(r'C:\Users\Dell\Desktop\minorproject\minorproject\djangobackend\models\sample\1-rose-black-spot-geoff-kiddscience-photo-library.jpg')