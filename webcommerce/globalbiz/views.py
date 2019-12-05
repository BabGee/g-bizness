from django.shortcuts import render, redirect, get_object_or_404
from category.models import Category
from product.models import Product, Order, OrderProduct
#from users.models import Address
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
#from users.forms import CheckoutForm, CouponForm


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


# class CheckoutView(View):
#     def get(self, *args, **kwargs):
#         try:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             form = CheckoutForm()
#             context = {
#                 'form': form,
#                 'couponform': CouponForm(),
#                 'order': order,
#                 'DISPLAY_COUPON_FORM': True
#             }

#             shipping_address_qs = Address.objects.filter(
#                 user=self.request.user,
#                 address_type='S',
#                 default=True
#             )
#             if shipping_address_qs.exists():
#                 context.update(
#                     {'default_shipping_station': shipping_station_qs[0]})

#             billing_address_qs = Address.objects.filter(
#                 user=self.request.user,
#                 address_type='B',
#                 default=True
#             )
#             if billing_address_qs.exists():
#                 context.update(
#                     {'default_billing_address': billing_address_qs[0]})

#             return render(self.request, "checkout.html", context)
#         except ObjectDoesNotExist:
#             messages.info(self.request, "You do not have an active order")
#             return redirect("core:checkout")

#     def post(self, *args, **kwargs):
#         form = CheckoutForm(self.request.POST or None)
#         try:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             if form.is_valid():

#                 use_default_shipping = form.cleaned_data.get(
#                     'use_default_shipping')
#                 if use_default_shipping:
#                     print("Using the defualt shipping address")
#                     address_qs = Address.objects.filter(
#                         user=self.request.user,
#                         address_type='S',
#                         default=True
#                     )
#                     if address_qs.exists():
#                         shipping_address = address_qs[0]
#                         order.shipping_address = shipping_address
#                         order.save()
#                     else:
#                         messages.info(
#                             self.request, "No default shipping address available")
#                         return redirect('core:checkout')
#                 else:
#                     print("User is entering a new shipping address")
#                     shipping_address1 = form.cleaned_data.get(
#                         'shipping_address')
#                     shipping_address2 = form.cleaned_data.get(
#                         'shipping_address2')
#                     shipping_country = form.cleaned_data.get(
#                         'shipping_country')
#                     shipping_zip = form.cleaned_data.get('shipping_zip')

#                     if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
#                         shipping_address = Address(
#                             user=self.request.user,
#                             street_address=shipping_address1,
#                             apartment_address=shipping_address2,
#                             country=shipping_country,
#                             zip=shipping_zip,
#                             address_type='S'
#                         )
#                         shipping_address.save()

#                         order.shipping_address = shipping_address
#                         order.save()

#                         set_default_shipping = form.cleaned_data.get(
#                             'set_default_shipping')
#                         if set_default_shipping:
#                             shipping_address.default = True
#                             shipping_address.save()

#                     else:
#                         messages.info(
#                             self.request, "Please fill in the required shipping address fields")

#                 use_default_billing = form.cleaned_data.get(
#                     'use_default_billing')
#                 same_billing_address = form.cleaned_data.get(
#                     'same_billing_address')

#                 if same_billing_address:
#                     billing_address = shipping_address
#                     billing_address.pk = None
#                     billing_address.save()
#                     billing_address.address_type = 'B'
#                     billing_address.save()
#                     order.billing_address = billing_address
#                     order.save()

#                 elif use_default_billing:
#                     print("Using the defualt billing address")
#                     address_qs = Address.objects.filter(
#                         user=self.request.user,
#                         address_type='B',
#                         default=True
#                     )
#                     if address_qs.exists():
#                         billing_address = address_qs[0]
#                         order.billing_address = billing_address
#                         order.save()
#                     else:
#                         messages.info(
#                             self.request, "No default billing address available")
#                         return redirect('core:checkout')
#                 else:
#                     print("User is entering a new billing address")
#                     billing_address1 = form.cleaned_data.get(
#                         'billing_address')
#                     billing_address2 = form.cleaned_data.get(
#                         'billing_address2')
#                     billing_country = form.cleaned_data.get(
#                         'billing_country')
#                     billing_zip = form.cleaned_data.get('billing_zip')

#                     if is_valid_form([billing_address1, billing_country, billing_zip]):
#                         billing_address = Address(
#                             user=self.request.user,
#                             street_address=billing_address1,
#                             apartment_address=billing_address2,
#                             country=billing_country,
#                             zip=billing_zip,
#                             address_type='B'
#                         )
#                         billing_address.save()

#                         order.billing_address = billing_address
#                         order.save()

#                         set_default_billing = form.cleaned_data.get(
#                             'set_default_billing')
#                         if set_default_billing:
#                             billing_address.default = True
#                             billing_address.save()

#                     else:
#                         messages.info(
#                             self.request, "Please fill in the required billing address fields")

#                 payment_option = form.cleaned_data.get('payment_option')

#                 if payment_option == 'S':
#                     return redirect('core:payment', payment_option='stripe')
#                 elif payment_option == 'P':
#                     return redirect('core:payment', payment_option='paypal')
#                 else:
#                     messages.warning(
#                         self.request, "Invalid payment option selected")
#                     return redirect('core:checkout')
#         except ObjectDoesNotExist:
#             messages.warning(self.request, "You do not have an active order")
#             return redirect("core:order-summary")


