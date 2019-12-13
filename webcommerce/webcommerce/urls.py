"""webcommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as users_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from globalbiz.views import (
    ProductList,
    productdetail,
    CategoryList, 
    categorydetail, 
    add_to_cart, 
    remove_from_cart, 
    remove_single_product_from_cart,
    OrderSummaryView,
    CheckoutView,
    AddCouponView,
    SearchResultsView
    )
   


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('globalbiz.urls')),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('register', users_views.register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('logout', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('products/', ProductList.as_view(template_name='globalbiz/productlist.html')),
    path('products/<int:pk>/', productdetail, name='product-detail'),
    path('categorys/', CategoryList.as_view(template_name='globalbiz/categorylist.html'), name='category'),
    path('categorys/<int:pk>/', categorydetail, name='category-detail'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),
    path('remove-product-from-cart/<int:pk>/', remove_single_product_from_cart, name='remove-single-product-from-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
     ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

