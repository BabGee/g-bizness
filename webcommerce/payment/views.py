from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from product.models import Order
from django.views.decorators.csrf import csrf_exempt
from product.models import Order

@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')

@csrf_exempt
def payment_canceled(request):   
    return render(request, 'payment/canceled.html')

@csrf_exempt
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, order_id)
    host = request.get_host()

    paypal_dict = {
        'business' : settings.PAYPAL_RECEIVER_EMAIL,
        'ammount' : order.get_total(),
        'prod_name' : f'Order {order.pk}',
        'invoice' : str(order.pk),
        'currency_code' : 'USD',
        'notify_url' : 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url' : 'http://{}{}'.format(host,reverse('payment:done')),
        'cancel_return' : 'http://{}{}'.format(host,reverse('payment:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {
        'order' : order,
        'form' : form
    }
    return render(request, 'payment/process.html', context)  
