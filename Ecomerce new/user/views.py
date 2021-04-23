import os
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponse
from django.contrib import messages
from order.models import OrderInfo,OrderProduct,Wishlist
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile

from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db import connection

#restframe work token genrate           
from rest_framework.authtoken.models import Token

 

def profile(request):
    if request.method =='POST':
        user_form = UserUpdateForm(request.POST,instance= request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance = request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            if request.FILES.get('image',None) != None:
                try:
                    os.remove(request.user.image.url)
                except Exception as e:
                    messages.success(request,"Exception in removing old profile image:",e)
                request.user.image = request.FILES['image']
                request.user.save()
            messages.success(request,'Your account has been updated')
            return HttpResponseRedirect('/user/profile')
    else:
        user_form = UserUpdateForm(instance= request.user)
        profile_form = ProfileUpdateForm(instance = request.user.userprofile)

    current_user = request.user
    profile = UserProfile.objects.get(user_id = current_user.id)
    wishlist = Wishlist.objects.filter(user_id = current_user.id)
    context = {'user_form':user_form,'profile_form':profile_form,
    'profile':profile,'wishlist':wishlist}

    return render(request,'profile.html',context)


def user_orders(request):
    current_user = request.user
    orders = OrderInfo.objects.filter(user_id = current_user.id).order_by('id')
    profile = UserProfile.objects.get(user_id = current_user.id)
    shop = OrderProduct.objects.filter(user_id = current_user.id)
    
    
    page = request.GET.get('page')
    print(page)

    paginator = Paginator(orders,5)
    print (orders)  #pagination start in search page
    try:
        orders = paginator.page(page)
        print(orders)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
        print(orders)

    context = {'profile':profile,
               'orders':orders,
               'shop':shop,
               
               }
    return render (request,'user_order.html',context)


from user.tokens import account_activate_token
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text
from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.views.generic import View


def signup_form(request):
    if request.method =='POST':
        name = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.error(request,"Passwords do not match")
            return HttpResponseRedirect('/')
            
        else:
            user =  User.objects.create_user(username=name,email=email,password=password1)
            token,created = Token.objects.get_or_create(user=user)
          

            user.save()
            current_user = user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = 'Images/user/userprofile.jpg'
            data.save()
            # current_site=get_current_site(request)
            # subject = "Your account is activate"
            # message = render_to_string('account_activation_email.html',{
            #     'user':user,
            #     'domain':current_site.domain,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':account_activate_token.make_token(user),

            # })
            # user.email_user(subject, message)
            # messages.success(request, 'Please confirm your email')
            messages.success(request, 'Succesfully register user. You can login')
            return HttpResponseRedirect('/')
    return render('/')

class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and account_activate_token.check_token(user, token):
            user.is_active = True

            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ("Your account has been confirmed"))
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,("the confirmation link was invaild, possibly becouse it has "))
            return HttpResponseRedirect('/')
    

def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id = current_user.id)
            request.session['userimage'] = userprofile.image.url
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')

    return HttpResponseRedirect('/')

def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')


def password(request):
    if request.method =='POST':
        form = PasswordChangeForm (request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Your password has suucessfully update')
            return HttpResponseRedirect('/user/profile')

        else:
            messages.error(request,'Please correct the error below. <br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')

    else:
        form = PasswordChangeForm(request.user)
        current_user = request.user
        profile = UserProfile.objects.get(user_id = current_user.id)
        current_user = request.user
        return render(request,'password.html',{'form':form,'profile':profile})