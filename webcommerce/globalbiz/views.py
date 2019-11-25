from django.shortcuts import render
from category.models import Category
from product.models import Product

def home(request):
    context = {
        'products' : Product.objects.all(), 
        'categories': Category.objects.all(),
        'newProducts' : Product.objects.filter(rating__name='New'),
        'offers' : Product.objects.filter(rating__name='Offer')
    }
    return render(request, 'globalbiz/index.html', context)


def macbook(request):
    context = {}

    return render(request, 'globalbiz/products/mac.html', context)


