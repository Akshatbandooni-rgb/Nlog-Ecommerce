from django.contrib import admin
from shop.models import Catogery, Brand, ShopProduct, ShopOrders, ProductQuantity

# Register your models here.
admin.site.register((Catogery, Brand, ShopProduct,
                     ShopOrders, ProductQuantity))
