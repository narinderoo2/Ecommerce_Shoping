from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/',views.about,name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('show_product/<int:id>/', views.show_product, name='show_product'),
    path('comment/<int:id>', views.comment, name='comment'),
    path('likepost/<int:id>/', views.like, name='like_post'),
]
