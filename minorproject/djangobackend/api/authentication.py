from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        validated_token = self.get_validated_token(self.get_raw_token(request))
        user_id = validated_token[api_settings.USER_ID_FIELD]
        # Ensure the user_id is an integer before querying the database
        user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: int(user_id)})
        return (user, validated_token)
