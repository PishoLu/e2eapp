from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path("user/", views.user_list),
    path("user/<int:pk>", views.user_detail),
    path("gettoken/", views.gettoken)
]
