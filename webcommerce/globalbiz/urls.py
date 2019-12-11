from django.urls import path
from . import views 


urlpatterns = [
    #pages path
    path('', views.home, name='globalbiz-home'),
    path('about', views.about_us, name='about-us'),
    path('contact', views.contact, name='contact'),
    path('howToShop', views.how_to_shop, name='how-to-shop'),
    path('howToPay', views.how_to_pay, name='how-to-pay'),
    path('deliveryTimeline', views.delivery_timeline, name='delivery-timeline'),
    path('returnsRefunds', views.returns_refunds, name='returns-refunds'),
]