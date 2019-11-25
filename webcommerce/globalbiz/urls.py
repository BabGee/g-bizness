from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='globalbiz-home'),
    path('Macbook Pro New', views.macbook, name='globalbiz-mac'),
]