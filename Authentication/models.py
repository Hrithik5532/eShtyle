#Authentication/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    is_verified = models.BooleanField(default=False)  # Add this line
    otp = models.IntegerField(default=0)  # Add this line
    
    is_creator = models.BooleanField(default=False)  # Indicates if the user has activated a Creator account
    bank_details = models.TextField(blank=True, null=True)  # You might want to structure this more securely or use a separate model
    ifsc_code = models.CharField(blank=True, null=True)  # You might want to structure this more securely or use a separate model
    id_proof = models.CharField(max_length=20, blank=True, null=True)  # Aadhar or PAN
    payment_made = models.BooleanField(default=False) 
    
    
    