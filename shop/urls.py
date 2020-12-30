"""Nlog_Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.urls import path, include
from shop import views

urlpatterns = [

    path('', views.index, name='shopHome'),
    path('about', views.aboutUs, name='aboutus'),
    path('catogery/<str:slug>', views.catogries, name='catogery'),
    path('filter', views.filterByBrand, name='filterbybrand'),
    path('managecart', views.manageCart, name='managecart'),
    path('displaycart', views.displaycart, name='displaycart'),
    path('clearcart', views.clearcart, name='clearcart'),
    path('removeproduct', views.removeProductFromCart, name='removeproduct'),
    path('checkout', views.checkout, name='checkout'),
    path('orders', views.displayOrders, name='displayorders'),
    path('<str:sku>', views.productBySku, name='productbysku'),




]
