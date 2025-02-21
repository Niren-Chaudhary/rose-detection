import cv2
import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def load_images(rose_path, notrose_path, img_size):
    images = []
    labels = []

    # Load rose images
    for filename in os.listdir(rose_path):
        img = cv2.imread(os.path.join(rose_path, filename))
        img = cv2.resize(img, (img_size, img_size))
        images.append(img)
        labels.append(1)  # Label '1' for rose

    # Load notrose images
    for filename in os.listdir(notrose_path):
        img = cv2.imread(os.path.join(notrose_path, filename))
        img = cv2.resize(img, (img_size, img_size))
        images.append(img)
        labels.append(0)  # Label '0' for not rose

    images = np.array(images)
    labels = np.array(labels)
    
    # Normalize images
    images = images / 255.0

    return images, labels

def load_disease_images(healthy_path, black_spot_path, mildew_path, img_size):
    images = []
    labels = []

    # Load healthy rose images
    for filename in os.listdir(healthy_path):
        img = cv2.imread(os.path.join(healthy_path, filename))
        img = cv2.resize(img, (img_size, img_size))
        images.append(img)
        labels.append(0)  # Label '0' for healthy

    # Load black spot rose images
    for filename in os.listdir(black_spot_path):
        img = cv2.imread(os.path.join(black_spot_path, filename))
        img = cv2.resize(img, (img_size, img_size))
        images.append(img)
        labels.append(1)  # Label '1' for black spot

    # Load mildew rose images
    for filename in os.listdir(mildew_path):
        img = cv2.imread(os.path.join(mildew_path, filename))
        img = cv2.resize(img, (img_size, img_size))
        images.append(img)
        labels.append(2)  # Label '2' for mildew

    images = np.array(images)
    labels = np.array(labels)

    # Normalize images
    images = images / 255.0

    return images, labels
