import uuid
import string
import random
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from home.models import Product, Variants


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField()
    comment = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.product.title
        
    @property
    def price(self):
        return (self.product.price)

    @property
    def amount(self):
        return (self.quantity * self.product.price)

    @property
    def varamount(self):
        return (self.variant.price * self.quantity)
    


    # @property
    # def promo_code(self,):
    #     n=3
    #     # res = ''.join(random.choices(string.ascii_uppercase + string.digits,k = self.price))
    #     # res = ''.join(string.ascii_uppercase + string(self.price))
        
    #     res = self.product.title[:8:4] + self.variant.size.name[:2] + self.variant.color.name[:2].join(string.ascii_uppercase[:3] + string.digits[:2])
    #     return res

class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']


class OrderInfo(models.Model):
    STATUS =(
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preaparing', 'Preaparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    code = models.CharField(max_length=5, editable=False)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.CharField(max_length=50, null=True,blank=True)
    phone = models.CharField(max_length=20,blank=True)
    address = models.CharField(blank=True,max_length=150)
    city = models.CharField(blank=True,max_length=20)
    country = models.CharField(blank=True,max_length=20)
    total = models.FloatField()
    status = models.CharField(max_length=10 , choices=STATUS,default='New')
    ip = models.CharField(max_length=100,blank=True)
    adminnote = models.CharField(max_length=100,blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

class OrderForm(ModelForm):
    class Meta:
        model = OrderInfo
        fields = ['first_name','last_name','address','phone','city','country','email']


class Payment(models.Model):
    STATUS =(
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preaparing', 'Preaparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    card_number = models.IntegerField()
    full_name = models.CharField(max_length=50)
    last_month = models.CharField(max_length=10)
    cvc = models.IntegerField(null=True,blank=True)
    email = models.CharField(max_length=20,blank=True)
    password = models.CharField(max_length=20,blank=True)
    status = models.CharField(max_length=10 , choices=STATUS,default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['card_number','full_name','last_month','cvc','email','password']




class OrderProduct(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Canceled','Canceled'),
    )
    order = models.ForeignKey(OrderInfo,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, blank=True ,null=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS,default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(null=True,blank=True)
    create_at = models.DateTimeField(auto_now_add=True,null=True)


    def __str__(self):
        return self.product.title

class WishlistForm(ModelForm):
    class Meta:
        model = Wishlist
        fields = ['quantity']
