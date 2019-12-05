from django.shortcuts import render, redirect, get_object_or_404
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



def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


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

                    if is_valid_form([delivery_address, delivery_station]):
                        delivery_address = Address(
                            user=self.request.user,
                            street_address=delivery_address,
                            station=delivery_station
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
                    pass
                    #return redirect('payment', payment_option='Mpesa')
                elif payment_option == 'P':
                    pass
                   # return redirect('payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("order-summary")
