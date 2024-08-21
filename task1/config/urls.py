"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.shortcuts import render,HttpResponse

user_list = [
    {'name':'송미현', 'age':20},
    {'name':'신지호', 'age':12},
    {'name':'신지민', 'age':6},
    {'name':'강아지', 'age':2},
    {'name':'고양이', 'age':5},
]

def index(request):
    return HttpResponse('<h1>hello2</h1>')

def users(request):
    return render(request,'users.html',{'users':user_list})

def user_info(request,num):

    user = user_list[num-1]

    return render(request,'user.html',{'user':user})
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('users/', users),
    path('user/<int:num>',user_info),

]
