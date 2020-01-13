from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views


urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path("gettoken/", views.gettoken),
    # message操作
    path("store_message/", views.store_message),
    path("filter_messages/<int:pk>", views.filter_messages),
    path("message_parse/", views.message_parse),
    # user操作
    path("store_user/", views.store_user),
    path("get_user/<int:pk>", views.get_user),
    # friends操作
    path("store_friend/", views.store_friend),
    path("friends_list/", views.friends_list),
    path("friends_list/<int:pk>", views.friend_detail),
    # 获取三对新的密钥
    path('create_new_keyspair/', views.create_new_keyspair),
    # 检测私钥格式是否正确
    path("check_pri/", views.check_pri),
    path("encrypt_message/", views.encrypt_message),
    path("decrypt_message/", views.decrypt_message)
]
