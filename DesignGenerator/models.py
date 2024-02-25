
#DesignGenerator/models.py
from django.db import models
from Authentication.models import User
# Create your models here.

class Portfolio(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio_images')
    likes = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    used_by = models.IntegerField(default=0)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
