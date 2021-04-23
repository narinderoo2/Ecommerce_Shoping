from django import template
from django.db.models import Sum
from django.http import request
from django.urls import reverse
from home.models import Product

from main import settings
from order.models import ShopCart, OrderInfo,Wishlist,OrderProduct

register = template.Library()



@register.simple_tag
def product_departments():
    return Product.objects.all().order_by('id')[:6]


@register.simple_tag
def shopcart(userid):
    shopcart = ShopCart.objects.filter(user_id = userid).all()
    return shopcart


@register.simple_tag
def shopcartcount(userid):
    count = ShopCart.objects.filter(user_id = userid).count()
    return count

@register.simple_tag
def totalshop(userid):
    shopcart = ShopCart.objects.filter(user_id =  userid).all()
    total= 0
    for ps in shopcart:
        if ps.product.variant == 'None':
            total += ps.product.price * ps.quantity
        else:
            total += ps.variant.price * ps.quantity

    return total


@register.simple_tag
def whishlist(userid):
    wishlist = Wishlist.objects.filter(user_id = userid).count()
    return wishlist


@register.simple_tag
def order(userid):
    orders = OrderInfo.objects.filter(user_id = userid).count()
    return orders


