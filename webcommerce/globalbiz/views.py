from django.shortcuts import render, redirect, get_object_or_404
from category.models import Category
from product.models import Product, Order, OrderProduct
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin

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

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'globalbiz/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order product is in the order
        if order.products.filter(product__pk=product.pk).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, "This product quantity was updated.")
            return redirect("order-summary")
        else:
            order.products.add(order_product)
            messages.info(request, "This product was added to your cart.")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, "This product was added to your cart.")
        return redirect("order-summary")

@login_required
def remove_single_product_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order product is in the order
        if order.products.filter(product__pk=product.pk).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.products.remove(order_product)
            messages.info(request, "This product quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This product was not in your cart")
            return redirect("product", pk=pk)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product", pk=pk)


@login_required
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order product is in the order
        if order.products.filter(product__pk=product.pk).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(order_product)
            messages.info(request, "This product was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This product was not in your cart")
            return redirect("product-detail", pk=pk)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product-detail", pk=pk)
