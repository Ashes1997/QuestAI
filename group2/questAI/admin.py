from django.contrib import admin
from questAI.models import Products, Baskets, Comments, Reviews, Purchase


# Register your models here.
admin.site.register(Products)
admin.site.register(Comments)
admin.site.register(Reviews)
admin.site.register(Baskets)
admin.site.register(Purchase)
from questAI.models import UserProfile

admin.site.register(UserProfile)
