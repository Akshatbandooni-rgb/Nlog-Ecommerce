from django.db import models
from django.conf import settings
import datetime

# Create your models here.


class Catogery(models.Model):
    catogery_id = models.AutoField(primary_key=True)
    catogery_name = models.CharField(max_length=50)

    def __str__(self):
        return self.catogery_name


class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    catogery = models.ForeignKey(Catogery, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class ShopProduct(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    price = models.IntegerField(default=0)
    catogery = models.ForeignKey(Catogery, on_delete=models.CASCADE, null=True)
    product_sku = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    registered_date = models.DateField()
    productimage = models.ImageField(
        upload_to='shop/images', default='/default/default.png')

    def __str__(self):
        return self.product_name


class ShopOrders(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(ShopProduct)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=150, default="")
    phone = models.CharField(max_length=150, default="")
    date = models.DateField(default=datetime.datetime.today)
    iscompleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.order_id)


class ProductQuantity(models.Model):
    order = models.ForeignKey(ShopOrders,  on_delete=models.CASCADE)
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField()
