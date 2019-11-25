from django.shortcuts import render
from category.models import Category
from product.models import Product

def home(request):
    context = {
        'products' : Product.objects.all(), #'' : Product.objects.filter(ratings__name='Biggest discount')
        'categories': Category.objects.all()
    }
    return render(request, 'globalbiz/index.html', context)
