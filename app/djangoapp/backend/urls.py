from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views


urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path('get_live/', views.get_live),
    path("gettoken/", views.gettoken),
    path('user/', views.user_list),
    path('user/<int:pk>', views.user_detail),
    path('create_new_keyspair', views.create_new_keyspair)
]
