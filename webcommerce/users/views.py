from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .forms import UserRegisterForm
#from django.contrib.auth.decorators import login_required
#from .models import Profile
#from shopping_cart.models import Order


def register(request):
	if request.method == "POST":
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get("username")
			messages.success(request, f"Account created for {username} You can now login")
			return redirect("login")
	else:
		form = UserRegisterForm()

	context = {
		"form":form
	}
	return render(request, "users/register.html", context)