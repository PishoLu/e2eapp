from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('get_info', views.get_info),
    path('login', views.login),
    path('register', views.register),
    path("gettoken", views.gettoken),
    path("user",views.user_list),
    path("user/<int:pk>",views.user_detail)
]
