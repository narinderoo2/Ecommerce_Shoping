from django.urls import path
from user import views
from .views import ActivateAccount

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('orders/', views.user_orders, name='user_orders'),
    path('password/', views.password, name='password'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
]

