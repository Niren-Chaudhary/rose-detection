from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # This remains unchanged
    name = 'api'

    def ready(self):
        # MongoEngine doesn't require changing the AppConfig directly,
        # but you can include additional setup like signals or database connections if necessary.
        import mongoengine
        # You can add MongoEngine initialization here, if needed
        # Example: mongoengine.connect('your_database_name')
