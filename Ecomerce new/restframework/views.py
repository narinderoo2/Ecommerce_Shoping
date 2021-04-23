from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.models import User
from restframework.serializers import ResisterSerializer,PostSerializer,EmailVerificationSerializer
from rest_framework.authtoken.models import Token
from rest_framework import generics,status
from rest_framework.decorators import api_view,permission_classes,APIView
from rest_framework.response import Response
from home.models import Product

# authentications
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes,authentication_classes


# for token as a authentication
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication


# error meaage show in home page 
from django.contrib import messages
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
import jwt

from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text
from restframework.tokens import api_account_activate_token
from django.views.generic import View


class RegisterView(generics.GenericAPIView):
    serializer_class = ResisterSerializer
    queryset = User.objects.all()

    def post(self, request, *args , **kwargs):
        if request.method =='POST':
            serializer = self.get_serializer(data=request.data)
            data = {}
            if serializer.is_valid():
                account = serializer.save()

                current_site=get_current_site(request)
                subject = "Your Api account is activate"
                message = render_to_string('verify_email.html',{
                    'user':account.username,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(account.pk)),
                    'token':api_account_activate_token.make_token(account),

                })
                account.email_user(subject, message)

                # user_data = serializer.data
                # user = User.objects.get(email =user_data['email'])
                # current_site = get_current_site(request).domain
                
                # subject = "Your Api account is active "

                # uid = urlsafe_base64_encode(force_bytes(account.pk))
                # token = api_account_activate_token.make_token(account)
                # sendLink = reverse('activate_email')
                
                # absurl = 'http://'+current_site+sendLink+token
                # email_body = 'Hi' +user.username + " User link to verify your email " +absurl
                # data ={'email_body':email_body,'to_email':user.email,'email_subject':subject}
                # Util.send_email (data)

                # user_data = serializer.data
                # user = User.objects.get(email =user_data['email'])
                # token1 = RefreshToken.for_user(user).access_token
                # current_site = get_current_site(request).domain
                # relativeLink = reverse('verify')
                
                # absurl = 'http://'+current_site+relativeLink+"?token="+str(token1)
                # email_body = 'Hi' +user.username + "Use link to verify your email\n" + absurl
                # data={'email_body':email_bo dy, 'to_email': user.email ,'email_subject':'Verify your email'}
                # Util.send_email(data)


                data['Success'] = "Welcome to new user. Your account has been successfull create"
                data['username'] = account.username
                data['email'] = account.email
                data['password'] = account.password
                token,created = Token.objects.get_or_create(user=account)
                data['token'] = token.key
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)


class VerifyEmail(generics.GenericAPIView):
    def get(self, request,uidb64, token, *args, **kwargs):
        data={}
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and api_account_activate_token.check_token(user, token):
            user.is_active = True

            user.profile.email_confirmed = True
            user.save()

            data['response'] = "Your account has been confirmed"
            return Response(data, status=status.HTTP_200_OK)
        else:
            data['response'] = "Invaild token, log in with other account"
            return Response(status=status.HTTP_404_NOT_FOUND)


# token fuction create
class ObtainAuthTokenView(APIView):
    authentication_classes=[]
    permission_classes=[]
    
    def post(self,request):
        context={}
        username = request.POST.get('username')
        password = request.POST.get('password')
        account = authenticate(username=username, password=password)

        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            context ['response'] = "Successfully authenticated"
            context['pk'] = account.pk
            context['email']=account.email
            context['token'] = token.key
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid creadentails'
        return Response(context)



def api_about(request):
    current_user = request.user
    if current_user.is_authenticated:
        token =  Token.objects.get(user=request.user)
        context={
        'token':token}
        return render(request, 'api.html',context)
    else:
        messages.error(request,"Without login , not allowed user in this page")
        return HttpResponseRedirect('/')

class PostView(generics.GenericAPIView):
    serializer_class = PostSerializer
    queryset = Product.objects.all()
    permission_classes =[IsAuthenticated]

    def post(self, request,*args, **kwargs):
        post = Product.objects.all()
        user = request.user
        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            data={}
            if serializer.is_valid():
                serializer.save()
                data['response']='Your post is submit succesfully'
                return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# update of post
@api_view(['PUT',])
@permission_classes ((IsAuthenticated,))
def post_update(request,id):
    
    try:
        post = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    current_user = request.user
    if request.method =='PUT':
        serializer = PostSerializer(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            data ['response'] = 'UPDATE_SUCCESS'
            data['category_name'] = post.category_name
            data['title']=post.title
            data['heading']=post.heading
            data['price'] = post.price
            data['shiping'] = post.shiping
            data['image1'] = post.image1
            return Response(data=data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


