from django.db import models
from category.models import Category
from django.urls import reverse
from django.contrib.auth.models import User

class Rating(models.Model):
    name =  models.CharField(max_length=120)
    description = models.TextField() 

    def __str__(self):
        return self.name

class Product(models.Model):
    image = models.ImageField(default='default.jpg', upload_to='product_pics')
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, default=None, null=True)
    
    def __str__(self):
        return f'{self.title} Category: {self.category}'

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={
            'pk': self.pk
        })

    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={
            'pk': self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={
            'pk': self.pk
        })


class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_discount_product_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_total_product_price() - self.get_total_discount_product_price()

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_product_price()
        return self.get_total_product_price()


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    products = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a billing address
    (Failed checkout)
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_final_price()
        
        return total

