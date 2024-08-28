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
from audioop import reverse

from django.contrib import admin
from django.urls import path,include
from blog import views
from member import views as member_views
from django.views.generic import TemplateView, RedirectView
from django.views import View
from django.shortcuts import redirect,render
from blog import cb_views

#
# class AboutView(TemplateView):
#     template_name = 'about.html'
#
# # def test_view(request):
# #     if request.method == 'POST':
# #         ...
# #     else
# #         ...
# class TestView(View):
#     def get(self, request):
#         return render(request, 'test_get.html')
#     def post(self,request):
#         return render(request, 'test_post.html')
#

urlpatterns = [
    path('admin/', admin.site.urls),



    # auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.sign_up, name='signup'),

    path('login/',member_views.login, name='login'),

    path('',include('blog.urls')),
#     # 클래스베이스뷰어
#     # path('about/',TemplateView.as_view(template_name = 'about.html'),name='about'),
#
#     path('about/', AboutView.as_view(), name='about'),  #위에 클래스를 불러와서 사용
#
#     path('redirect/', RedirectView.as_view(pattern_name='about'), name='redirect'),
#     # path('redirect2', lambda req: redirect('about')),
#
#     path('test/', TestView.as_view(),name='test')

    # CBV blog (클래스베이스뷰 블로그)

    path('fb/',include('blog.fbv_urls')),

]
