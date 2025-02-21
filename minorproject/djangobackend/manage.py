#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import tensorflow as tf

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangobackend.settings')

    # Set the path for the fine-tuned rose model
    rose_model_path = r'C:\Users\Dell\Desktop\minorproject\minorproject\djangobackend\models\fine_tuned_rose_model.keras'

    # Check if the model file exists before loading
    if not os.path.exists(rose_model_path):
        raise FileNotFoundError(f"Model file not found: {rose_model_path}")
    
    # Load the model
    try:
        rose_model = tf.keras.models.load_model(rose_model_path)
        print(f"Successfully loaded the model from {rose_model_path}")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise e

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
