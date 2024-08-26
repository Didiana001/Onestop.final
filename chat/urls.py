from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('signup/', views.signup_view, name='signup'),
    path('accounts/login/', views.custom_login_view, name='login'),
    path('accounts/logout/', views.custom_logout_view, name='logout'),
]