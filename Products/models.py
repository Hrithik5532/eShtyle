from django.db import models
from Authentication.models import User
from DesignGenerator.models import Portfolio
# Create your models here.

import uuid


class SQP(models.Model):
    
    color = models.CharField(max_length=200)
    price = models.IntegerField()
    size = models.CharField(max_length=200)
    
    def __str__(self):
        return self.color + " " + str(self.price) + " " + self.size
    
    
    
class AllProducts(models.Model):
    name = models.CharField(max_length=200)
    sqp = models.ManyToManyField(SQP)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(AllProducts, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE,blank=True, null=True)

    quantity = models.IntegerField()
    sqp = models.ManyToManyField(SQP)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
    
class wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(AllProducts, on_delete=models.CASCADE,blank=True, null=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    
