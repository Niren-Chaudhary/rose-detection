import os
import uuid
import random
import string
import numpy as np
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail import send_mail
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from mongoengine import connect, Document, StringField
import json
from datetime import timedelta
import tensorflow as tf
import cv2
from .serializers import LoginSerializer, RegisterSerializer
from django.http import JsonResponse
from .serializers import ImageUploadSerializer
from PIL import Image
from django.core.files.storage import default_storage

# Connect to MongoDB (adjust connection settings for production)
connect('rosedata', host='mongodb+srv://ravipant1122:1122@cluster0.ef1rf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

# Define User model using MongoEngine
class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)

    def set_password(self, password):
        # Use bcrypt or another hashing method here in production
        self.password = password
        self.save()

    def check_password(self, password):
        # Add password check logic (e.g., bcrypt verification)
        return self.password == password

# Load pre-trained models for image classification
rose_model = tf.keras.models.load_model(r'C:\Users\Dell\Desktop\minorproject\minorproject\djangobackend\models\fine_tuned_rose_model.keras')
disease_model = tf.keras.models.load_model(r'C:\Users\Dell\Desktop\minorproject\minorproject\djangobackend\models\fine_tuned_disease_model.keras')
img_size = 128

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (img_size, img_size))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# DRF login view with token generation using SimpleJWT
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            'message': 'Login successful!',
            'access': access_token,
            'refresh': refresh_token,
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DRF signup view with token generation using SimpleJWT
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user (authenticated or not) to access signup
def signup_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({
            'message': 'User registered successfully!',
            'token': access_token,
            'user_id': str(user.id),
            'email': user.email,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DRF Password Reset View using email instead of username
@api_view(['POST'])
def password_reset_view(request):
    data = request.data
    email = data.get('email')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    if not email or not new_password or not confirm_password:
        return Response({'error': 'Email, new password, and confirm password are required'}, status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm_password:
        return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the user exists
    user = User.objects.filter(email=email).first()
    if not user:
        return Response({'error': 'No user found with this email'}, status=status.HTTP_404_NOT_FOUND)

    # Reset the password
    user.set_password(new_password)
    return Response({'message': 'Password reset successful!'}, status=status.HTTP_200_OK)

# DRF logout view
@api_view(['POST'])
def logout_view(request):
    """Logout user and invalidate the JWT token."""
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
            except exceptions.TokenError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
@permission_classes([AllowAny])
def classify_image(request):
    # Ensure image is provided in the request
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image provided'}, status=400)

    image_file = request.FILES['image']
    
    # Define the media directory (from Django settings or custom path)
    MEDIA_DIR = settings.MEDIA_ROOT  # Use the MEDIA_ROOT setting defined in settings.py

    # Ensure the directory exists
    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)
    
    # Save the uploaded image
    image_path = os.path.join(MEDIA_DIR, image_file.name)
    with default_storage.open(image_path, 'wb+') as destination:
        for chunk in image_file.chunks():
            destination.write(chunk)

    # Preprocess and predict if the image is a rose or not
    img = cv2.imread(image_path)
    img_resized = cv2.resize(img, (128, 128))
    img_resized = img_resized / 255.0
    img_resized = np.expand_dims(img_resized, axis=0)

    # Predict using the rose model
    rose_prediction = rose_model.predict(img_resized)
    is_rose = rose_prediction[0][0] > 0.5  # Assuming the model outputs probabilities

    # If it is a rose, classify its disease status
    if is_rose:
        disease_prediction = disease_model.predict(img_resized)
        disease_class_idx = np.argmax(disease_prediction, axis=-1)  # Get the index of the class with the highest score
        disease_status = ['Healthy Rose', 'Black Spot', 'Mildew'][disease_class_idx[0]]
    else:
        disease_status = 'Not a Rose'

    # Clean up the temporary file
    os.remove(image_path)

    # Return the results as JSON
    return JsonResponse({'is_rose': bool(is_rose), 'disease_status': disease_status}, status=200)

# Manual signup view (non-DRF JSON handling)
def manual_signup_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # Check if user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already exists"}, status=400)

            # Create user
            user = User(username=username, email=email, password=password)
            user.set_password(password)
            user.save()

            # Create token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return JsonResponse({
                "message": "User registered successfully!",
                "token": access_token,
                "user_id": str(user.id),
                "email": user.email,
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)


# Simple test views for direct responses (optional)
def signup(request):
    return JsonResponse({"message": "Signup successful!"})

def manual_signup(request):
    return JsonResponse({"message": "Manual Signup successful!"})

def login(request):
    return JsonResponse({"message": "Login successful!"})
