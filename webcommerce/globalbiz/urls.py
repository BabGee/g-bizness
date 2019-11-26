from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='globalbiz-home'),
    path('Macbook Pro New', views.macbook, name='globalbiz-mac'),
    path('Jeep New Model 2019', views.jeep, name='globalbiz-jeep'),
]