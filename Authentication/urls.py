from django.urls import path
from .views import *

urlpatterns = [
path('auth/register', UserRegistrationAPIView.as_view(), name='register'),
path('auth/login', LoginAPIView.as_view(), name='login'),
path('auth/verify-otp', OTPVerificationAPIView.as_view(), name='verify-otp'),
path('auth/google', GoogleLoginView.as_view(), name='google_login'),
path('profile', UserProfile, name='google_login'),
path('mail-verification', verify_mail, name='verify_mail'),
path('forgot-password', forgot_password, name='forgot_password'),

# path('all-images',),
path('activate-creator-account/', CreatorAccountActivationAPIView.as_view(), name='activate-creator-account'),

path('suggestions', suggestions, name='suggestions'),
path('filter-by-tags', filter_by_tags, name='filter_by_tags'),

path('virtually-tried', virtually_tried, name='virtually_tried'),
    # Add paths for login and reset password as you implement them
    
    path('waitlist',waitlist, name='waitlist'),
]
