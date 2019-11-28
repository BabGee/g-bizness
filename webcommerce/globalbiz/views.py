from django.shortcuts import render
from category.models import Category
from product.models import Product

# views.py
from django.views.generic import ListView
from django.shortcuts import render
from product.models import Product

class ProductList(ListView):
    model = Product


#******************pages.html ***********************************
def home(request):
    context = {
        'products' : Product.objects.all(), 
        'categories': Category.objects.all(),
        'newProducts' : Product.objects.filter(rating__name='New'),
        'offers' : Product.objects.filter(rating__name='Offer')
    }
    return render(request, 'globalbiz/index.html', context)

def productdetail(request,pk):
    context = {
        'product': Product.objects.get(pk = pk)
    }
    return render(request, 'globalbiz/product.html', context)


