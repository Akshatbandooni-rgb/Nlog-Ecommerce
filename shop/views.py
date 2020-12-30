from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from shop.models import Catogery, Brand, ShopOrders, ShopProduct, ProductQuantity
from django.contrib import messages
from math import ceil
from shop.middlewares.authMiddleware import isLoggedInMiddleware
from django.utils.decorators import method_decorator

# Create your views here.


def index(request):
    catogries = Catogery.objects.all()
    products = ShopProduct.objects.all()
    querysetSize = len(products)
    slidesNum = querysetSize//4 + ceil((querysetSize/4)-(querysetSize)//4)

    context = {"products": products,
               'slidesNum': slidesNum, 'range': range(1, slidesNum), 'catogries': catogries}

    return render(request, 'shop/shopHome.html', context)


def aboutUs(request):
    return render(request, 'shop/aboutus.html')


def catogries(request, slug):
    global currcatogery
    currcatogery = slug
    catogries = Catogery.objects.all()
    catogery = Catogery.objects.filter(catogery_name=slug).first()
    catogeryId = Catogery.objects.get(catogery_name=slug).catogery_id
    brands = Brand.objects.filter(catogery=catogery)
    products = ShopProduct.objects.filter(catogery=catogery)
    context = {'currentcatogery': catogery,
               'products': products, 'catogries': catogries, 'brands': brands}
    return render(request, 'shop/catogery.html', context)


def productBySku(request, sku):
    product = ShopProduct.objects.filter(product_sku=sku).first()
    catogries = Catogery.objects.all()
    context = {'product': product, 'catogries': catogries}
    return render(request, 'shop/productBySku.html', context)


def filterByBrand(request):
    if request.method == "POST":
        global currcatogery
        filterbrand = request.POST["brand"]
        filtercatogery = request.POST["catogery"]
        brand = Brand.objects.get(name=filterbrand)
        catogery = Catogery.objects.filter(catogery_name=currcatogery).first()

        catogeryId = Catogery.objects.get(
            catogery_name=currcatogery).catogery_id
        brandId = brand.brand_id
        catogries = Catogery.objects.all()
        brands = Brand.objects.all()
        products = ShopProduct.objects.filter(
            catogery=catogeryId, brand=brandId)
        context = {'products': products,
                   'catogries': catogries, 'currentcatogery': catogery, 'brands': brands}
        return render(request, 'shop/catogery.html', context)
    return HttpResponse("Error:404 Forbidden")


def manageCart(request):
    catogries = Catogery.objects.all()
    context = {'catogries': catogries}
    if request.method == "POST":
        productid = request.POST['productid']
        remove = request.POST['remove']
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(productid)
            if remove == "True":
                if quantity > 1:
                    quantity = quantity-1
                    cart[productid] = quantity
                else:
                    quantity = quantity-1
                    cart[productid] = quantity
                    cart.pop(productid)
            else:
                if quantity:
                    cart[productid] = quantity+1
                else:
                    cart[productid] = 1

        else:
            cart = {}
            cart[productid] = 1
        request.session['cart'] = cart
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def reducequantity(request):
    if request.method == "POST":
        productid = request.POST['productid']
        cart = request.session.get('cart')
        quantity = cart.get(productid)
        if quantity > 0:
            quantity = quantity-1
            cart[productid] = quantity
        else:
            cart.pop(productid)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def displaycart(request):
    cart = request.session.get('cart')
    if cart:
        productids = list(cart.keys())
        products = ShopProduct.objects.filter(product_id__in=productids)
        return render(request, 'shop/displaycart.html', {'products': products})
    return render(request, 'shop/displaycart.html')


def clearcart(request):
    cart = request.session.get('cart')
    if cart:
        del request.session['cart']
        request.session.modified = True
    return render(request, 'shop/displaycart.html')


def removeProductFromCart(request):
    if request.method == "POST":
        productid = request.POST['productid']
        cart = request.session.get('cart')
        if productid in cart.keys():
            cart.pop(productid)
            request.session.modified = True
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def checkout(request):
    if request.method == "POST":
        quantity = 0
        cartsum = 0
        curr_quantity = 0
        address = request.POST['address']
        contact = request.POST['contactno']
        current_user = request.user
        cart = request.session.get('cart')
        productids = list(cart.keys())
        prodlist = ShopProduct.objects.filter(product_id__in=productids)
        if cart:
            for i in cart:
                quantity = quantity + cart[i]
            for productid in cart:
                curr_quantity = cart[productid]
                product = ShopProduct.objects.filter(
                    product_id=productid).first()
                prod_price = product.price
                cartsum = cartsum+(prod_price*curr_quantity)

            order = ShopOrders(customer=current_user, price=cartsum, quantity=quantity,
                               address=address, phone=contact)
            order.save()
            order.products.add(*prodlist)
            for productid in cart:
                product = ShopProduct.objects.filter(
                    product_id=productid).first()
                productquantity = ProductQuantity(
                    order=order, product=product, quantity=cart[productid])
                productquantity.save()
            request.session['cart'] = {}
            request.session.modified = True
        return redirect('displaycart')


@isLoggedInMiddleware
def displayOrders(request):
    productlist = []
    orderpresent = False
    current_user = request.user
    orders = ShopOrders.objects.filter(customer=current_user)

    if orders:
        orderpresent = True
        for order in orders:

            # orderid = order.order_id
            productlist.append(order.products.all())
            # productset_by_order = order.products.all()
            # for product in productset_by_order:
            #     productid = product.product_id

    return render(request, 'shop/displayorders.html', {'productlist': productlist, 'orderpresent': orderpresent, 'orders': orders})
