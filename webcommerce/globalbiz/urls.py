from django.urls import path
from . import views

urlpatterns = [
    #pages path
    path('', views.home, name='globalbiz-home'),
]