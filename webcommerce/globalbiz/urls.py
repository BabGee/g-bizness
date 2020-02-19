from django.urls import path
from . import views 


urlpatterns = [
    #pages path
    path('', views.home, name='globalbiz-home'),
    path('about', views.about_us, name='about-us'),
    path('contact', views.contact, name='contact'),
]