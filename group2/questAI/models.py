from django.db import models
from django.contrib.auth.models import User
class Products (models.Model):
    productId = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=64, unique= True)
    productDescription = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    category = models.CharField(max_length=64)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.productName

class Baskets (models.Model):
    basketId = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    productId =models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    quantity= models.IntegerField(default=1)

def __str__(self):
    return str(self.basketId) + " " + str(self.productId.id) + " " + str(self.username)


class Reviews(models.Model):
    LIKE_CHOICES = (
        ('like', 'Like'),  # First element is the actual value, second is the human-readable name
        ('dislike', 'Dislike'),
    )
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    productId = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="Product")
    review_type = models.CharField(max_length=7, choices=LIKE_CHOICES, default='like', verbose_name="Like/Dislike")

    class Meta:
        unique_together = ('username', 'productId')
        verbose_name_plural = "Reviews"
    



class Comments (models.Model):
    commentId = models.AutoField(primary_key=True)
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
    

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User who purchased")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name="Purchased product")
    quantity = models.IntegerField(default=1, verbose_name="Quantity purchased")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Purchase date")

    class Meta:
        unique_together = ('user', 'product','purchase_date')
        verbose_name_plural = "Purchases"

    def __str__(self):
        return f"Purchase of {self.product.productName} by {self.user.username} on {self.purchase_date.strftime('%Y-%m-%d %H:%M:%S')}"