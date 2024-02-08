from django.urls import path
from questAI import views

app_name = 'questAI'

urlpatterns = [
path('', views.index, name='index'),
]

