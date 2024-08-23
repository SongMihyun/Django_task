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
from django.http import HttpRequest, HttpResponse, Http404
from django.urls import path
from django.shortcuts import render
from bookmark import views


movie_list = [
    {'title':'파묘','director':'장재현'},
    {'title':'윙카','director':'폴 킹'},
    {'title':'듄:파트2','director':'드니 빌뇌브'},
    {'title':'시민덕희','director':'박영주'}
]

book_list=[
    {'title':'세이노의 가르침','author':'세이노'},
    {'title':'해커스 토익 기출 VOCA','author':'데이비드'},
    {'title':'모순','author':'양귀자'},
    {'title':'5천 년 역사가 단숨에 이해되는 최소한의 한국사','author':'최태성'},
    {'title':'돈의 심리학','author':'모건 하우절'}
]

def index(request):
    return HttpResponse('<h1>hello2</h1>')


def books(request):
    return render(request,'books.html',{'books':book_list})

def book_detail(requset,index):
    if index > len(book_list) or index <=0:
        raise Http404

    book = book_list[index-1]
    context={'book':book, 'index':index}
    return render(requset,'book.html', context)


# def book_list(request):
#     book_text =''
#
#     for i in range(0,10):
#         book_text += f'book {i}<br>'
#     return HttpResponse(book_text)
#
# def book(request, num):
#     book_text =f'book {num}번 페이지 입니다.'
#     return HttpResponse(book_text)

def language(request, lang):
    return HttpResponse(f'<h1>{lang}언어 페이지입니다.')

# def movies(request):
#     movie_titles = [
#         f'<a href="/movie/{index}/">{movie['title']}</a><br>'
#         for index,movie in enumerate(movie_list)]
#
#     # movie_titles = []
#     # for movie in movie_list:
#     #     movie_titles.append(movie['title'])
#     response_text = ''
#     for index,title in enumerate(movie_titles):
#         response_text += f'<a href="/movie/{index}/">{title}</a><br>'
#
#     return HttpResponse(response_text)

def movies(request):
    # from django.shortcuts import render
    return render(request, 'movies.html',{'movie_list':movie_list})

def movie_detail(request, index):
    if index > len(movie_list) -1:
        # from django.http import Http404
        raise Http404

    movie = movie_list[index]

    # response_text = f'<h1>{movie['title']}<p>감독: {movie['director']}<p>'
    # return HttpResponse(response_text)

    # return render(request, 'movie.html', {'movie':movie})

    # context = {'movie_list': movie_list, 'index': index}
    # return render(request, 'movie.html', context)

    context = {'m': movie, 'index': index}
    return render(request, 'movie.html', context)


def gugus(request):
    gugu_list=[x for x in range(1,10)]
    return render(request, 'gugus.html', {'gugus':gugu_list})

def gugu(request, x):
    num = x
    gugudan_list =[f'{x}*{y}={x*y}' for y in range(1,10)]
    return render(request, 'gugu.html', {'gugudans': gugudan_list, 'num':num})



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('books/',books),
    path('book/<int:index>',book_detail),
    # path('book/<int:num>',book_detail),
    path('book_list/<int:num>/',book_detail),
    path('language/<str:lang>/', language),
    path('movies/', movies),
    path('movie/<int:index>/', movie_detail),
    path('gugus/',gugus),
    path('gugu/<int:x>/',gugu),
    path('bookmark/', views.bookmark_list),
    path('bookmark/<int:pk>/', views.bookmark_detail),
]