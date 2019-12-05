from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from django_countries.fields import CountryField
# from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('M', 'MPESA'),
    ('P', 'PayPal')
)

DELIVERY_CHOICES = (
    ('S', 'Pick up Station'),
    ('H', 'Home or Office')
)

STATION_CHOICES = (
    ('CB', 'NAIROBI CBD'),
    ('WS', 'WESTLANDS'),
	('JG', 'UCHUMI JOGOO ROAD'),
	('GC', 'GARDEN CITY'),
	('MS', 'MOMBASA CBD'),
	('KS', 'KISUMU CBD'),
	('NK', 'NAKURU'),
)	


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	phone = forms.IntegerField()

	class Meta:
		model = User
		fields = ["username", "phone", "email", "password1", "password2"]



# class CheckoutForm(forms.Form):
#     first_name = forms.CharField(required=True)
# 	last_name = forms.CharField(required=True)
# 	mobi_number = forms.IntegerField(required=True)
#     delivery_address = forms.CharField(required=False)
#     shipping_station =forms.CharField(label='Pick up station', widget=forms.Select(choices=STATION_CHOICES))
# 	delivery_option = forms.ChoiceField(
#         widget=forms.RadioSelect, choices=DELIVERY_CHOICES)
#     payment_option = forms.ChoiceField(
#         widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


# class CouponForm(forms.Form):
#     code = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Promo code',
#         'aria-label': 'Recipient\'s username',
#         'aria-describedby': 'basic-addon2'
#     }))
