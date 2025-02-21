from rest_framework import serializers
from .models import CustomUser, UploadedImage
from mongoengine.errors import ValidationError, NotUniqueError

# Signup Serializer for MongoEngine
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_username(self, value):
        # Clean the username to remove unwanted characters
        return value.strip().replace('\n', '')

    def validate_email(self, value):
        # Clean the email to remove unwanted characters
        return value.strip().replace('\n', '')

    def create(self, validated_data):
        try:
            # Create a new user object
            user = CustomUser(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            user.set_password(validated_data['password'])
            user.save()  # Save to MongoDB
            return user
        except NotUniqueError:
            raise serializers.ValidationError("Username or email already exists.")
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        except Exception as e:
            raise serializers.ValidationError(f"An error occurred: {str(e)}")

# Login Serializer for MongoEngine
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()  # Ensure email is a valid email field
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        # Clean the email value
        return value.strip().replace('\n', '')

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            # Try to find the user by email
            user = CustomUser.objects.get(email=email)
            
            # Validate the password
            if not user.check_password(password):
                raise serializers.ValidationError("Invalid email or password.")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User not found with this email.")
        except Exception as e:
            raise serializers.ValidationError(f"An unexpected error occurred: {str(e)}")

        return {
            'user': user  # Return the validated user
        }

# Image Upload Serializer for Django ORM model
class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ['image']
