from django.urls import path
from questAI import views

app_name = 'questAI'

urlpatterns = [
path('', views.index, name='index'),
path('home/', views.home, name='home'),
path('login/', views.login, name='login'),
path('signup/', views.signup, name='signup'),
path('basket/', views.basket, name='basket'),
path('topup/', views.topup, name='topup'),
path('checkout/', views.checkout, name='checkout')
]

