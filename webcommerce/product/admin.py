from django.contrib import admin
from .models import Product, Rating, Order, OrderProduct

admin.site.register(Product)
admin.site.register(Rating)
admin.site.register(Order)
admin.site.register(OrderProduct)
