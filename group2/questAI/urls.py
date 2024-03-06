from django.urls import path
from questAI import views

app_name = 'questAI'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    # path('login/', views.login, name='login'),
    # path('signup/', views.signup, name='signup'),
    path('basket/', views.basket, name='basket'),
    path('topup/', views.topup, name='topup'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/',views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('manage/', views.manage, name='manage'),
    path('add/', views.add, name='add'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]

