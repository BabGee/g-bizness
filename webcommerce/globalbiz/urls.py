from django.urls import path
from . import views

urlpatterns = [
    #pages path
    path('', views.home, name='globalbiz-home'),
    #products path
    path('Macbook Pro New', views.macbook, name='globalbiz-mac'),
    path('Jeep New Model 2019', views.jeep, name='globalbiz-jeep'),
    #categories path
    path('Electronics', views.electronics, name='globalbiz-electronics'),
    path('Furniture', views.furniture, name='globalbiz-furniture'),
]