from mongoengine import Document, StringField
from django.contrib.auth.hashers import make_password, check_password

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
