from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)#该实例与USer实例为一对一关系，on_delete=models.CASCADE表明关联的user实例被删除后该实例也自动被删除
    address = models.CharField(max_length=512)
    postcode=models.CharField(max_length=32)
    # website = models.URLField(blank=True)#blank=True允许该字段在表单中为空，即用户可以不提供
    # picture = models.ImageField(upload_to='profile_images',blank=True)#upload_to='profile_images'指定上传图片将被保存到的目录

    def __str__(self):
        return self.user.username