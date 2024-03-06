from django.db import models
from django.contrib.auth.models import User
class Products (models.Model):
    # productId= models.IntegerField(unique=True)
    productId = models.AutoField(primary_key=True)

    productName = models.CharField(max_length=64, unique= True)
    productDescription = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    category = models.CharField(max_length=64)
    # image_path = models.URLField()
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.productName

class Baskets (models.Model):
    productId = models.AutoField(primary_key=True)
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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)#This instance has a one-to-one relationship with the USer instance. on_delete=models.CASCADE indicates that the instance will be automatically deleted after the associated user instance is deleted.
    address = models.CharField(max_length=512)
    postcode=models.CharField(max_length=32)
    # website = models.URLField(blank=True)#blank=TrueAllow this field to be empty in the form, that is, the user does not need to provide
    # picture = models.ImageField(upload_to='profile_images',blank=True)#upload_to='profile_images'Specify the directory where uploaded images will be saved

    def __str__(self):
        return self.user.username