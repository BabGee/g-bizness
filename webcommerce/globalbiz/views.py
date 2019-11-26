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
    context = {
        'mac' : Product.objects.filter(title='Macbook Pro New').first()
    }
   
    return render(request, 'globalbiz/products/mac.html', context)

def jeep(request):
    context = {
        'jeep' : Product.objects.filter(title='Jeep New Model 2019').first()
    }
   
    return render(request, 'globalbiz/products/jeep.html', context)
