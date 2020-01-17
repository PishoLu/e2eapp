from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views


urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    path("gettoken/", views.gettoken),
    # message操作
    path("storeMessage/", views.storeMessage),
    path("filterMessages/<int:pk>", views.filterMessages),
    # path("message_parse/", views.message_parse),
    # user操作
    path("storeUser/", views.storeUser),
    path("getUser/<int:pk>", views.getUser),
    # friends操作
    path("storeFriend/", views.storeFriend),
    path("friendsList/", views.friendsList),
    path("friendsList/<int:pk>", views.friend_detail),
    # 获取三对新的密钥
    path('createNewKeyspair/', views.createNewKeyspair),
    # 检测私钥格式是否正确
    path("checkPri/", views.checkPri),
    path("encryptMessage/", views.encryptMessage),
    path("decryptMessage/", views.decryptMessage)
]
