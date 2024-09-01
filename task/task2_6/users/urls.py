from django.urls import path
from django.urls import include

from users import views

app_name = 'users'
urlpatterns = [
    # login
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),

]