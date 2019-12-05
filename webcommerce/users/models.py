from django.db import models
from django.contrib.auth.models import User

# class Address(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	mobi_number = models.IntegerField(max_length=10)
#     delivery_address = models.CharField(max_length=100)
#     shipping_station = models.CharField(max_length=100)
#     default = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.username

#     class Meta:
#         verbose_name_plural = 'Addresses'

