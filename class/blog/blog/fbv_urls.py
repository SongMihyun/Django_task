from django.urls import path

from blog import views

app_name = 'fb'
urlpatterns =[
    # FBV blog (펑션베이스뷰 블로그)
    path('', views.blog_list, name='list'),
    # path('blogs/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='detail'),
    path('create/', views.blog_create, name='create'),
    path('blog/<int:pk>/update/', views.blog_update, name='update'),
    path('blog/<int:pk>/delete/', views.blog_delete, name='delete'),

]