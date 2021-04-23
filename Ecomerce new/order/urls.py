from django.urls import path
from . import views

urlpatterns = [
    path('shopcart/', views.shopcart, name='shopcart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('review/', views.review, name='review'),
    path('thanku/', views.thanku, name='thanku'),

    path('addtoshopcart/<int:id>', views.addtoshopcart, name='addtoshopcart'),
    path('addtowishlist/<int:id>', views.addtowishlist, name='addtowishlist'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('deletefromwishlist/<int:id>', views.deletefromwishlist, name='deletefromwishlist'),


]
