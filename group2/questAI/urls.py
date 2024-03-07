from django.conf.urls.static import static
from django.urls import path

from group2 import settings
from questAI import views

app_name = 'questAI'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('basket/', views.basket, name='basket'),
    path('topup/', views.topup, name='topup'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/',views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('add-product/', views.add_product, name='add_product'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('manage-home/',views.manage_home, name='manage_home'),
    path('edit-product/<int:product_id>', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>', views.delete_product, name='delete_product'),
    path('add_to_basket/<int:product_id>/', views.add_to_basket, name='add_to_basket'),
    path('update_basket/', views.update_basket, name='update_basket'),
    path('search-product/',views.search_product,name='search_product')

]

