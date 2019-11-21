from django.shortcuts import render
from .models import Category
from product.models import Product

def testrt(request): 
    context = {
        'categories' : Category.objects.all(),
        'products' : Product.objects.all()
    }
    return render(request, 'testApp/test.html', context)


def electrons(request):
    context = {
        'electronics' : Product.objects.filter(category__name='Electronics'),
        'products' : Product.objects.filter(category__name='Electronics'.price())
    }
    return render(request, 'testApp/electrons.html', context)
