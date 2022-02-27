from . import views
from django.urls import path

urlpatterns = [
    # path('process', views.payment_process, name='process'),
    path('done', views.payment_done, name='done'),
    path('canceled', views.payment_canceled, name='canceled'),
]