"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from order import views as OrderViews
from user import views as UserViews


from django.conf.urls import handler404

handler404 = 'home.views.error_404_view'
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('auth/',include('rest_framework.urls')),
    path('order/', include('order.urls')),
    path('user/', include('user.urls')),
    path('api/', include('restframework.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('shopcart/', OrderViews.shopcart, name='shopcart'),
    path('login/', UserViews.login_form, name='login_form'),
    path('logout/', UserViews.logout_func, name='logout_func'),
    path('signup/', UserViews.signup_form, name='signup_form'),

    path('ajaxcolor/',views.ajaxcolor,name='ajaxcolor'),
    path('search_filter/',views.search_filter,name='search_filter'),


    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
