from django import template
from product.models import Order

register = template.Library()


@register.filter
def cart_product_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].products.count()
    return 0
