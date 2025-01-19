import random
import string
from rest_framework.permissions import AllowAny
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
from .serializers import LoginSerializer, RegisterSerializer

# Connect to MongoDB (for development, adjust connection settings for production)
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
        # SimpleJWT logout functionality by blacklist
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

# DRF Image upload view
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can upload
def image_upload_view(request):
    image = request.FILES.get('image')  # Get the uploaded image from the request
    if image:
        # Process the image here (you can skip saving to DB)
        # For now, just returning a success response with the image name
        return Response({
            "message": "Image uploaded successfully",
            "image_name": image.name
        }, status=status.HTTP_200_OK)
    return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

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

# # OTP Generation View
# @api_view(['POST'])
# def generate_otp(request):
#     # Extract email from the request data
#     email = request.data.get('email')

#     if not email:
#         return Response({'error': 'Email is required'}, status=400)

#     # Generate a random 6-digit OTP
#     otp = ''.join(random.choices(string.digits, k=6))

#     # Store the OTP in the cache (expires in 5 minutes)
#     cache.set(email, otp, timeout=timedelta(minutes=5))

#     # Send the OTP via email
#     subject = 'Your OTP for Password Reset'
#     message = f'Your OTP for password reset is: {otp}'
#     from_email = 'your_email@gmail.com'  # Use your email here

#     try:
#         send_mail(subject, message, from_email, [email])
#         return Response({'message': 'OTP sent to your email!'})
#     except Exception as e:
#         return Response({'error': str(e)}, status=500)

# # OTP Validation View
# @api_view(['POST'])
# def validate_otp(request):
#     # Extract email and OTP from the request data
#     email = request.data.get('email')
#     otp_entered = request.data.get('otp')

#     if not email or not otp_entered:
#         return Response({'error': 'Email and OTP are required'}, status=400)

#     # Get the OTP stored in cache
#     stored_otp = cache.get(email)

#     if not stored_otp:
#         return Response({'error': 'OTP has expired or does not exist'}, status=400)

#     if otp_entered == stored_otp:
#         return Response({'message': 'OTP validated successfully!'})
#     else:
#         return Response({'error': 'Invalid OTP'}, status=400)


# Simple test views for direct responses (optional)
def signup(request):
    return JsonResponse({"message": "Signup successful!"})

def manual_signup(request):
    return JsonResponse({"message": "Manual Signup successful!"})

def login(request):
    return JsonResponse({"message": "Login successful!"})
