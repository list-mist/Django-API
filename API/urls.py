"""user URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.register),
    path('login/',views.loginUser),
    path('details/',views.details),
    path('logout/',views.logoutUser),
    path('edit/',views.editDetails),
    path('DRF/',views.DRF_view),
    path('AddData',views.AddData),
    path('EditData',views.EditData),
    path('userList',views.userList.as_view()),
    path('userList/<int:pk>',views.userList.as_view()),
    path('userListMixin',views.userListMixin.as_view()),
    path('userEditMixin/<int:pk>',views.userEditMixin.as_view()),
    path('userListGen',views.userListGen.as_view()),
    path('userEditGen/<int:pk>',views.userEditGen.as_view()),
   
]
