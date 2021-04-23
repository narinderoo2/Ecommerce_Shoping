# from django.http import HttpResponseRedirect, JsonResponse

from django.urls import reverse
from order.models import ShopCart
from user.models import UserProfile
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from home.models import Product, CommentForm, Comment, Like_User,Variants,Image,ContactForm,Contact
from django.template.loader import render_to_string
from home.forms import SearchForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# send emnail
from django.core.mail import send_mail

from django.contrib import messages

 
def home(request):
    product = Product.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    user = UserProfile.objects.filter(user_id = current_user.id)
    if user is None:
        messages.error(request,"you have not account, please login on web page")
        return HttpResponseRedirect('/')
       
    else:
        context ={'product':product,'shopcart':shopcart}
    
    return render(request,'home.html',context)

def show_product(request,id):
    query = request.GET.get('q')
    product = Product.objects.get(pk=id)
    product_related = Product.objects.all()[:4]
    images = Image.objects.filter(product_id = id)
    comment = Comment.objects.filter(product_id=id, status='New')
    context = {'product':product,
                    'product_related':product_related,
                    'comment':comment,
                    'images':images,}

    # have a varient in product
    if product.variant != 'None':
        if request.method == 'POST': # select color time(update time)
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id =variant_id)
            colors = Variants.objects.filter(product_id=id,size_id=variant.size_id)
            sizes = Variants.objects.raw('SELECT * FROM home_variants WHERE product_id=%s GROUP BY size_id',[id])
            query += variant.title + 'Size:' +str(variant.size) + 'Color:' + str(variant.color)

        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id = id,size_id=variants[0].size_id)
            sizes = Variants.objects.raw('SELECT * FROM home_variants WHERE product_id=%s GROUP BY size_id',[id])
            variant = Variants.objects.get(id=variants[0].id)
        context.update({'sizes':sizes,
                        'colors':colors,
                        'variant':variant,
                        'query':query,})
    return render(request, 'show_product.html',context)

# ajxx color and size change auto
def ajaxcolor(request):
    data = {}
    if request.POST.get('action') =='POST':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id = productid, size_id=size_id)
        context = {
            'size_id':size_id,
            'productid':productid,
            'colors':colors,
        }
        data = {'rendered_table':render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)

def like(request,id):
    product = Product.objects.get(id=id)
    print(product)
    user = request.user
    if request.method == 'POST':    
        
        post_id = request.POST.get('post_id')
        print(post_id)
        comment_obj = Comment.objects.get(id=post_id)
        print(comment_obj)
        product_obj = Product.objects.get(id=id)
        print(product_obj)


        if user in comment_obj.like.all() :
            comment_obj.like.remove(user)
        else:
            comment_obj.like.add(user)

        like,created = Like_User.objects.get_or_create(user1=user,product1=product, comment1=comment_obj)
        if not created:
            if like.value=='Like':
                like.value ='Unlike'
            else:
                like.value = 'Like'

        like.save()
    return redirect('show_product', id= product.pk)

def comment(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.name = form.cleaned_data['name']
            data.rate = form.cleaned_data['rate']
            data.comment = form.cleaned_data['comment']
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            product = Product.objects.all()
            current_user = request.user
            shopcart = ShopCart.objects.filter(user_id = current_user.id)

            query = form.cleaned_data['query']
            if query:
                products = Product.objects.filter(heading__icontains=query)
            else:
                products = Product.objects.filter(heading__icontains=query)
                
            save_heading = {'products':products,
                            'query':query,
                            'product':product,  'shopcart':shopcart
                            }
            return render(request,'search_grid.html',save_heading)
    return HttpResponseRedirect('/')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = Contact()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            # data.ip = request.META.get['SERVER_NAME']
            data.save()
            messages.success(request,"Your message has been sent, thanku you")
            return HttpResponseRedirect('/contact')
    form = ContactForm
    contaxt = {'form':form,
              }
    return render(request,'contact.html',contaxt)


def search_filter(request):
    context={   
    }
    return render(request,'search_grid.html',context)

def about (request):
    return render(request,'about.html')


def error_404_view(request,exception):
    return render(request,'error_404.html') 