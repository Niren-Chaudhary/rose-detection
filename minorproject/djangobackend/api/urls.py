from django.urls import path
from . import views

urlpatterns = [
    # Signup Views
    path('signup/', views.signup_view, name='signup'),                  # DRF Signup with Token Generation
    path('manual_signup/', views.manual_signup_view, name='manual_signup'),  # Manual Signup View

    # Login View
    path('login/', views.login_view, name='login'),                    # DRF Login with Token Generation

    # Password Reset View
    path('password-reset/', views.password_reset_view, name='password-reset'), 
     
    # path('send-otp/',views.generate_otp, name='send-otp'),
    # path('validate-otp/',views.validate_otp, name='validate-otp'),
     path('upload-image/', views.image_upload_view, name='upload-image'),
     path('logout/',views.logout_view, name='logout'),
]
 