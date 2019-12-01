from django.shortcuts import render, get_object_or_404
from category.models import Category
from product.models import Product

# views.py
from django.views.generic import ListView
from django.shortcuts import render
from product.models import Product


#******************pages.html ***********************************
def home(request):
    context = {
        'products' : Product.objects.all(), 
        'categories': Category.objects.all(),
        'newProducts' : Product.objects.filter(rating__name='New'),
        'offers' : Product.objects.filter(rating__name='Offer')
    }
    return render(request, 'globalbiz/index.html', context)

class ProductList(ListView):
    model = Product

def productdetail(request,pk):
    context = {
        'product': Product.objects.get(pk = pk)
    }
    return render(request, 'globalbiz/product.html', context)

class CategoryList(ListView):
    model = Category

def categorydetail(request,pk):
    cat = Category.objects.get(pk = pk)
    context = {
        'new_products_with_category': Product.objects.filter(category__name = cat, rating__name='New'),
        'offer_products_with_category': Product.objects.filter(category__name = cat, rating__name='Offer')
    }
    
    return render(request, 'globalbiz/category.html', context)
