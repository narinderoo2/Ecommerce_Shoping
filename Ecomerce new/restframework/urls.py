from django.urls import path
from restframework.views import RegisterView,ObtainAuthTokenView,PostView,post_update,VerifyEmail
from restframework import views

urlpatterns = [
    path('',views.api_about,name='api_about'),
    path('register/', RegisterView.as_view(),name="register"),
    path('login/',ObtainAuthTokenView.as_view(), name='login'),
    path('post/', PostView.as_view(),name="post"),
    path('post_update/<int:id>/', views.post_update,name="post_update"),
    path('activate_email/<uidb64>/<token>/',VerifyEmail.as_view(), name='activate_email'),

]

