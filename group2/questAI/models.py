from django.db import models
from django.contrib.auth.models import User
class Products (models.Model):
    productId= models.IntegerField(unique=True)
    productName = models.CharField(max_length=64)
    productDescription = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    category = models.CharField(max_length=64)
    image_path = models.URLField()

    def __str__(self):
        return self.productName

class Baskets (models.Model):
    basketId = models.IntegerField(unique=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    productId =models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    quantity= models.ImageField(default=1)

    def __str__(self):
        return self.basketId + " " + self.productId + " " + self.username

class Reviews (models.Model):
    reviewId= models.ImageField(unique=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    productId =models.ForeignKey(Products, on_delete=models.CASCADE)
    rating= models.IntegerField(default=1)
    
    def __str__(self):
        return self.reviewId

class Comments (models.Model):
    commentId = models.IntegerField(unique=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    productId =models.ForeignKey(Products, on_delete=models.CASCADE)
    commenttext = models.CharField(max_length=500)

    def __str__(self):
        return self.commentId
    

# Create your models here.
