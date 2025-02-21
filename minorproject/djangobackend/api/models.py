from mongoengine import Document, StringField
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# MongoDB CustomUser Model
class CustomUser(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)

    def set_password(self, password):
        # Use Django's password hashing method
        self.password = make_password(password)
        self.save()

    def check_password(self, password):
        # Check the password against the hashed password
        return check_password(password, self.password)

# MongoDB Folder Model
class Folder(Document):
    name = StringField(max_length=255, required=True)  # Name of the folder
    path = StringField(required=True)  # Path to the folder
    category = StringField(
        choices=[
            ('Rose', 'Rose'),
            ('NotRose', 'Not Rose'),
            ('Healthy', 'Healthy Leaf'),
            ('BlackSpot', 'Black Spot'),
            ('Mildew', 'Downy Mildew'),
        ],
        required=True
    )  # Folder category (e.g., Rose, Not Rose, etc.)

    def __str__(self):
        return self.name

# Django ORM Model for Image Upload (To handle image storage)
class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image uploaded on {self.uploaded_at}'
