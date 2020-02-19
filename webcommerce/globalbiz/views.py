from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from category.models import Category
from product.models import Product, Order, OrderProduct
from users.models import Address, Coupon
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import CheckoutForm, CouponForm
import random
import string
from django.db.models import Q 


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

#******************pages.html ***********************************
def home(request):
    products = Product.objects.all()
    context = {
        'products' : products, 
        'categories': Category.objects.all(),
        'newProducts' : Product.objects.filter(rating__name='New')[2:],
        '2newProducts' : Product.objects.filter(rating__name='New')[:2],
        'newProduct' : Product.objects.filter(rating__name='New').first()
    }
    return render(request, 'globalbiz/index.html', context)

class SearchResultsView(View):
    # model = Product
    # template_name = 'globalbiz/search_results.html'

    def get(self, *args, **kwargs):
        qs =  Product.objects.all()
        query1 = self.request.GET.get('qproduct')
        #qs = qs.filter(Q(title__icontains=query1))
        #query2 = self.request.GET.get('q2'), Product.objects.filter(Q(title__icontains=query1))!= '' and query1 is not None:
        if query1: 
            qs = qs.filter(Q(title__icontains=query1))
        if query1 == '':
            messages.warning(self.request, 'No Product selected')
            return redirect('/')
        if query1 is None:
            messages.warning(self.request, f'No Product Named{query1}')
            return redirect('/')

        context = {
            'search_query_rslt' : qs
        }
        return render(self.request, 'globalbiz/search_results.html', context) 

def about_us(request):
    return render(request, 'globalbiz/about.html')

def contact(request):
    context = {
        'offer_products' : Product.objects.filter(rating__name='Offer')[:4],
        'prod' : Product.objects.filter(rating__name='Offer').first()
    }
    return render(request, 'globalbiz/contact.html', context)    

class ProductList(ListView):
    model = Product

def productdetail(request,pk):
    product = Product.objects.get(pk = pk)
    cat = product.category
    context = {
        'product': product,
        'related_prod' : Product.objects.filter(category__name=cat)
    }
    return render(request, 'globalbiz/product.html', context)

class CategoryList(ListView):
    model = Category

def categorydetail(request,pk):
    cat = Category.objects.get(pk = pk)
    cats = Category.objects.all()
    context = {
        'products_with_category': Product.objects.filter(category__name = cat),
        'category' : cat,
        'other_cats' : cats
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
            messages.warning(self.request, 'You do not have an active order')
            return redirect('/')

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
        #check if the order product is in the order
        if order.products.filter(product__pk=product.pk).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, 'This product quantity was updated.')
            return redirect('order-summary')
        else:
            order.products.add(order_product)
            messages.info(request, 'This product was added to your cart.')
            return redirect('order-summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, 'This product was added to your cart.')
        return redirect('order-summary')

@login_required
def remove_single_product_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order product is in the order
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
            messages.info(request, 'This product quantity was updated.')
            return redirect('order-summary')
        else:
            messages.info(request, 'This product was not in your cart')
            return redirect('product', pk=pk)
    else:
        messages.info(request, 'You do not have an active order')
        return redirect('product', pk=pk)


@login_required
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        #check if the order product is in the order
        if order.products.filter(product__pk=product.pk).exists():
            order_product = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(order_product)
            messages.info(request, 'This product was removed from your cart.')
            return redirect('order-summary')
        else:
            messages.info(request, 'This product was not in your cart')
            return redirect('product-detail', pk=pk)
    else:
        messages.info(request, 'You do not have an active order')
        return redirect('product-detail', pk=pk)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("checkout")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            delivery_address_qs = Address.objects.filter(
                user=self.request.user,
                default=True
            )
            if delivery_address_qs.exists():
                context.update(
                    {'default_delivery_address': delivery_address_qs[0]})

            return render(self.request, "globalbiz/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                use_default_delivery = form.cleaned_data.get(
                    'use_default_delivery')
                if use_default_delivery:
                    print("Using the default delivery address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,    
                        default=True
                    )
                    if address_qs.exists():
                        delivery_address = address_qs[0]
                        order.delivery_address = delivery_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default delivery address available")
                        return redirect('checkout')
                else:
                    print("User is entering a new delivery address")
                    delivery_address = form.cleaned_data.get(
                        'delivery_address')
                    delivery_station = form.cleaned_data.get(
                        'delivery_station')
                    mobi_number = form.cleaned_data.get(
                        'mobi_number')    

                    if is_valid_form([delivery_address, delivery_station, mobi_number]):
                        delivery_address = Address(
                            user=self.request.user,
                            delivery_address=delivery_address,
                            shipping_station=delivery_station,
                            mobi_number=mobi_number
                        )
                        delivery_address.save()

                        order.delivery_address = delivery_address
                        order.save()

                        set_default_delivery = form.cleaned_data.get(
                            'set_default_delivery')
                        if set_default_delivery:
                            delivery_address.default = True
                            delivery_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required delivery address field")
                        return redirect('checkout')
    
                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'M':
                    return redirect(reverse('globalbiz-home'))
                    #return redirect('payment', payment_option='Mpesa')
                elif payment_option == 'P':
                    print('Hey')
                    #self.request.session['order_id'] = order.id
                    #return redirect(reverse('payment:process'))
                    #messages.add_message(self.request, messages.INFO, 'Order Placed!')
                    #return redirect('checkout')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("order-summary")
