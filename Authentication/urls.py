from django.urls import path
from .views import UserRegistrationAPIView, LoginAPIView, OTPVerificationAPIView

urlpatterns = [
    path('register', UserRegistrationAPIView.as_view(), name='register'),
        path('login', LoginAPIView.as_view(), name='login'),
path('verify-otp/', OTPVerificationAPIView.as_view(), name='verify-otp'),

    # Add paths for login and reset password as you implement them
]
