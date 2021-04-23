from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Avg
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe

from django.forms import ModelForm, TextInput


class Category(models.Model):
    category = models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category

class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    VARIANTS = (
        ('None','None'),
        ('Size','Size'),
        ('Color','Color'),
        ('Size-Color','Size-Color'),
    )
    category_name = models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    heading = models.CharField(max_length=200)
    price = models.IntegerField()
    slug = models.SlugField(null=False, unique=True)
    variant = models.CharField(max_length=10,choices=VARIANTS,default='None')
    status = models.CharField(max_length=10, choices=STATUS)
    detail = RichTextUploadingField()
    avaliable = models.BooleanField(default=False)
    image1 = models.FileField(upload_to='images')

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def count_review(self):  # comment count method == total comment of one post, so show the all count of comment
        add = Comment.objects.filter(product=self).aggregate(count=Count('id'))
        cnt = 0
        if add['count'] is not None:
            cnt = int(add['count'])
            return cnt

    def star_average(self): # one product avg of comment = data show in star function
        add = Comment.objects.filter(product = self).aggregate(average = Avg('id'))
        avg = 0
        if add['average'] is not None:
            avg = float(add['average'])
            return avg

    def image_tag(self):
        if self.image1.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image1.url))
        else:
            return ""


class Comment (models.Model):
    STATUS =(
        ('New' , 'New'),
        ('True' , 'True'),
        ('False' , 'False'),
    )
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,blank=True)
    comment = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    status = models.CharField(max_length=10 , choices=STATUS,default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name='comment_post',blank=True)

    def __str__(self):
        return self.name

    @property
    def man_like(self):
        return self.like.all().count()


# this comment form use in view.py in function of view
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'comment','rate']


LIKE_CHOICE=(
    ('Like','Like'),
    ('Unlike','Unlike'),
)


class Like_User(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE)
    product1 = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment1 = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True,blank=True)
    value = models.CharField(choices=LIKE_CHOICE, default='Like',max_length=10)
    vote = models.IntegerField(default=0)

    def __str__(self):
        return str(self.product1)

#image add in product multiple
class Image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(blank=True,upload_to='images/')

    def __str__(self):
        return self.title


# color code add with prodoct
class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, null=True,blank=True)

    def __str__(self):
        return self.name

    def color_code(self):
        if self.code is not None:
            return mark_safe('<p style="background-color: {}" > Color </p>'.format(self.code))
        else:
            return " "


# size of item (phone size,  cloth size, shoes size)
class Size (models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10,blank=True,null=True)

    def __str__(self):
        return self.name


# collect all data of user add in cart(product,size,color,price,etc)
class Variants(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    size = models.ForeignKey(Size,on_delete=models.CASCADE,null=True,blank=True)
    color = models.ForeignKey(Color,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=200,null=True,blank=True)
    image_id = models.IntegerField(null=True,blank=True,default=0)
    price = models.FloatField(default=0, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    def image_tag(self):
        img = Image.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage = ""
        return varimage

    def image(self):
        img = Image.objects.get(pk=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=20)
    message = models.TextField()
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject','message']
        widgets = {
            'name' : TextInput(attrs={'class': 'input form-control', 'placeholder' : 'Name & Surname'}),
            'email' : TextInput(attrs={'class': 'input form-control', 'placeholder' : 'email address'}),
            'phone' : TextInput(attrs={'class': 'input form-control', 'placeholder' : 'Phone Number'}),
            'subject' : TextInput(attrs={'class': 'input form-control', 'placeholder' : 'subject'}),
            'message' : TextInput(attrs={'class': 'input form-control', 'placeholder' : 'Your Message', 'rows':'5'}),
        }
