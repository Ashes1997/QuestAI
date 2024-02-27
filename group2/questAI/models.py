from django.db import models
from django.contrib.auth.models import User
class Products (models.Model):
    productId= models.IntegerField(unique=True)
    productName = models.CharField(max_length=64)
    productDescription = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    category = models.CharField(max_length=64)
    image_path = models.URLField()

class Baskets (models.Model):
    basketId = models.IntegerField(unique=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    productId =models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity= models.ImageField(default=1)

class Reviews (models.Model):
    reviewId= models.ImageField(unique=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    productId =models.ForeignKey(Products, on_delete=models.CASCADE)
    rating= models.IntegerField(default=1)

class Comments (models.Model):
    commentId = models.IntegerField(unique=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    productId =models.ForeignKey(Products, on_delete=models.CASCADE)
    commenttext = models.CharField(max_length=500)
    

# Create your models here.
