from django.shortcuts import render
from category.models import Category
from product.models import Product

def home(request):
    context = {
        'categories': Category.objects.all(),
        'products' : Product.objects.all()
    }
    return render(request, 'globalbiz/index.html', context)
