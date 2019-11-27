from django.shortcuts import render
from category.models import Category
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


#****************** product details.html ***********************************

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

#****************** Categories.html ***********************************

def electronics(request):
    context = {
        'newElectronics' : Product.objects.filter(category__name='Electronics', rating__name='New'),
        'offerElectronics' : Product.objects.filter(category__name='Electronics', rating__name='Offer')
    }
   
    return render(request, 'globalbiz/category/electronics.html', context)

def furniture(request):
    context = {
        'newFurn' : Product.objects.filter(category__name='Furniture', rating__name='New'),
        'offerFurn' : Product.objects.filter(category__name='Furniture', rating__name='Offer')
    }
   
    return render(request, 'globalbiz/category/furniture.html', context)
