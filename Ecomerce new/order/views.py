from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.utils.crypto import get_random_string
from order.models import (
    ShopCart, ShopCartForm, OrderForm,
    OrderInfo, OrderProduct, PaymentForm,
    Payment,Variants,Wishlist,WishlistForm
)
from user.models import UserProfile
from home.models import Product
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# for debit card condition
from itertools import groupby
import re

@login_required(login_url='/')
def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    variantid = request.POST.get('variantid')
    checkvariant = ShopCart.objects.filter(variant_id=variantid)

    checkproduct = ShopCart.objects.filter(product_id=id)
    if checkproduct and checkvariant:
        control = 1
    else:
        control = 0

    if request.method =='POST':
        form =ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:
                try:
                    data = get_object_or_404(ShopCart,product_id=id)
                    data.quantity += form.cleaned_data['quantity']
                    data.save()
                    
                except (ObjectDoesNotExist, MultipleObjectsReturned):
                    messages.error(request,'it is minimum order, Plese select other order')
                    return HttpResponseRedirect('/')

            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
        return HttpResponseRedirect(url)
    else:
        if control == 1:
            data = ShopCart.objects.get(product_id=id)
            data.quantity +=1
            data.save()
        else:
            data =ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id=None
            data.save()
        return HttpResponseRedirect(url)
   

def shopcart(request):
    product = Product.objects.all()
    current_user = request.user
    shpcart = ShopCart.objects.filter(user_id = current_user.id)
    if request.method =='POST':
        comment = request.POST['comment']
        add = shpcart(comment=comment)
        add.save()
    page = request.GET.get('page',1)

    paginator = Paginator(shpcart,4)  #pagination start in search page
    try:
        shpcart = paginator.page(page)
    except PageNotAnInteger:
        shpcart = paginator.page(1)
    except EmptyPage:
        shpcart = paginator.page(paginator.num_pages)

    count = ShopCart.objects.filter(user_id = current_user.id).count()

    if count == 0: 
        return HttpResponseRedirect('/')
    else:
        total = 0
        for ps in shpcart:
            if ps.product.variant == 'None':
                total += ps.product.price * ps.quantity
            else:
                total += ps.variant.price * ps.quantity
        
    context = {'shpcart':shpcart, 'total':total,'product':product}
    return render(request,'shop_cart.html',context)


def addtowishlist(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checkproduct = Wishlist.objects.filter(product_id=id)

    if checkproduct:
        control = 1
    else:
        control = 0

    if request.method =='POST':
        form =WishlistForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = Wishlist.objects.get(product_id=id)
                data.save()

            else:
                data = Wishlist()
                data.user_id = current_user.id
                data.product_id = id
                data.save()
        return HttpResponseRedirect('/order/wishlist')
    else:
        if control == 1:
            data = Wishlist.objects.get(product_id=id)
            data.quantity +=1
            data.save()
        else:
            data =ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1   
            data.save()
        return HttpResponseRedirect(url)


def wishlist(request):
    product = Product.objects.all()
    current_user = request.user  
    count = Wishlist.objects.filter(user_id = current_user.id).count()

    if count == 0: 
        messages.error(request,"You have no product in wishlist")
        return HttpResponseRedirect('/')
   
    else:
        profile = UserProfile.objects.get(user_id = current_user.id)
        shpcart = Wishlist.objects.filter(user_id = current_user.id)
        context = {'product':product, 'shpcart':shpcart,'profile':profile}
    return render(request,'wishlist.html',context)



def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request,"Your item deleted form ShopCart")
    return HttpResponseRedirect('/shopcart/')

def deletefromwishlist(request,id):
    Wishlist.objects.filter(id=id).delete()
    messages.success(request,"Your item deleted form ShopCart")
    return HttpResponseRedirect('/order/wishlist')


def checkout(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    count = ShopCart.objects.filter(user_id = current_user.id).count()

    if count == 0: 
        return HttpResponseRedirect('/')
    else:
        total = 0
        for ps in shopcart:
            if ps.product.variant == 'None':
                total += ps.product.price * ps.quantity
            else:
                total += ps.variant.price * ps.quantity
        
    if request.method =='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = OrderInfo()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.address = form.cleaned_data['address']
            data.user_id = current_user.id
            data.total = total
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            schopcart = ShopCart.objects.filter(user_id=current_user.id)
            for ps in schopcart:
                detail = OrderProduct()
                detail.order_id = data.id
                detail.product_id = ps.product_id
                detail.user_id = current_user.id
                detail.quantity = ps.quantity

                if ps.product.variant == 'None':
                    detail.price  =  ps.product.price
                else:
                    detail.price  =  ps.variant.price

                detail.variant_id = ps.variant_id

                if ps.product.variant == 'None':
                    detail.amount  =  ps.amount
                else:
                    detail.amount  =  ps.varamount
                detail.save()

                if ps.product.variant == 'None': 
                    product = Product.objects.get(id=ps.product_id)
                    product.save()
                
                else:
                    variant = Variants.objects.get(id=ps.product_id)
                    variant.quantity -= ps.quantity
                    variant.save()

            
            messages.success(request, 'Your Order has been completed. Thakes You')
            return HttpResponseRedirect("/order/payment")
            
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/checkout")

    form = OrderForm()
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    order = OrderProduct.objects.filter(user_id = current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'order':order,
            'shopcart':shopcart,
            'profile':profile,
            'form':form,
            'total':total}
    return render(request,'checkout.html',context)



def payment(request):
    current_user= request.user
    order = ShopCart.objects.filter(user_id = current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    count = ShopCart.objects.filter(user_id = current_user.id).count()

    if count == 0: 
        return HttpResponseRedirect('/')
    else:
        add_value = 0
        for ps in order:
            add_value += int(ps.price) * ps.quantity

    if request.method =='POST':
        card_number =  request.POST['card_number']
        full_name =  request.POST['full_name']
        last_month =  request.POST['last_month']
        cvc =  request.POST['cvc']

        if len(card_number) <= 11 or len(card_number) >= 13:
            messages.error(request,"Card Number is not correct")
        elif len(full_name) <= 5:
            messages.error(request,"Please enter more than 6 letter not correct")

            return HttpResponseRedirect('/order/payment')

        data = Payment(card_number=card_number, full_name=full_name, last_month=last_month,cvc=cvc)
        data.save()
        messages.success(request, 'Your Order has been completed. Thakes You')
        return HttpResponseRedirect("/order/review")

   
    context = {'order':order,'profile':profile,'add_value':add_value,}
    return render(request,'payment.html',context)


def review(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    profile = UserProfile.objects.filter(user_id = current_user.id)
    payment = Payment.objects.filter(create_at__lte=timezone.now()).order_by('create_at')[:1]
    count = ShopCart.objects.filter(user_id = current_user.id).count()

    if count == 0: 
        return HttpResponseRedirect('/')
    else:
        total = 0
        for ps in shopcart:
            if ps.product.variant == 'None':
                total += ps.product.price * ps.quantity
            else:
                total += ps.variant.price * ps.quantity

    context = {'payment':payment,
            'shopcart':shopcart,
            'total':total,
            'profile':profile}
    return render(request,'review.html',context)

def thanku(request):
    current_user = request.user
    count = ShopCart.objects.filter(user_id = current_user.id).count()

    if count == 0: 
        return HttpResponseRedirect('/')
    else:
        ShopCart.objects.filter(user_id=current_user.id).delete()

        request.session['cart_items'] = 0
    context = {
                'shopcart':shopcart,
                }
    return render(request,'thanku.html',context)