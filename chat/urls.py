from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),  # Handle the root URL
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('chat/', views.chat_view, name='chat'),
    path('home/', views.index_view, name='home'),  # Redirect to index_view for home
    path('courses/', views.courses_view, name='courses'),
    path('format-guide/', views.format_guide_view, name='format_guide'),
    path('askonestop/', views.askonestop_view, name='askonestop'),
    path('letter-list/<str:letter_category>/', views.letter_list, name='letter_list'),

]