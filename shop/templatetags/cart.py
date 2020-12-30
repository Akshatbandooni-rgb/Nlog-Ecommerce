from django import template
from shop.models import ProductQuantity

register = template.Library()


@register.filter(name='isIncart')
def isProductInCart(product, cart):
    print(cart)
    productId = str(product.product_id)
    print(productId)
    if productId in cart:
        return True
    return False


@register.filter(name='cartCount')
def cartCountByProduct(product, cart):
    productId = str(product.product_id)
    return cart[productId]


@register.filter(name='totalCartCount')
def totalCartCount(cart):
    sum = 0
    if cart:
        for i in cart:
            sum = sum + cart[i]
    return sum


@register.filter(name='isEmpty')
def isEmpty(cart):
    print(cart)
    sum = totalCartCount(cart)
    print(sum)
    if sum > 0:
        return False
    return True


@register.filter(name='cartPrice')
def cartPrice(products, cart):
    price = 0
    for product in products:
        quantity = cartCountByProduct(product, cart)
        price = price+(product.price*quantity)
        print(price)
    return price


@register.filter(name='productquantity')
def productQuantity(product, order):
    orderid = order.order_id
    prodquantity = ProductQuantity.objects.filter(order=order).filter(
        product=product).first()
    if prodquantity:
        return prodquantity.quantity
    return 0


@register.filter(name='belongsToOrder')
def belongsToOrder(product, order):
    orderid = order.order_id
    prodquantity = ProductQuantity.objects.filter(order=order).filter(
        product=product).first()
    if prodquantity:
        return True
    return False


@register.filter(name='priceByQuantity')
def priceByQuantity(product, order):
    price = product.price
    quantity = productQuantity(product, order)
    return price*quantity
