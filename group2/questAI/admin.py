from django.contrib import admin
from questAI.models import Products, Baskets, Comments, Reviews


# Register your models here.
admin.site.register(Products)
admin.site.register(Comments)
admin.site.register(Reviews)
admin.site.register(Baskets)