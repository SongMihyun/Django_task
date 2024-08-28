from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.transaction import commit
from django.http import Http404
from django.urls import reverse
from django.db.models import Q


from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from blog.forms import BlogForm
from blog.models import Blog


def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')

    q=request.GET.get('q')

    if q:
        # blogs = blogs.filter(title__icontains=q)
        # blogs = blogs.filter(content__icontains=q)
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        )

    # 페이지네이션
    paginator = Paginator(blogs, 10)
    page = request.GET.get('page')
    page_object = paginator.get_page(page)

    # visits = int(request.COOKIES.get('visits', 0)) + 1
    # request.session['count'] = request.session.get('count', 0) + 1

    context = {
        'object_list': page_object.object_list,
        'page_obj': page_object
    }

    response = render(request, 'blog_list.html', context)
    # response.set_cookie('visits', visits)

    return response

def blog_detail(request, pk):
    blog = Blog.objects.get(id=pk)
    context = {
        'blog': blog,
        'test': 'TEST'
               }
    return render(request,'blog.html', context)

# 블로그 생성페이지
@login_required()   #셋팅즈에 내가 설정해놓은 LOGIN_URL 로 자동으로 가짐
def blog_create(request):
    # if not request.user.is_authenticated:
    #     return redirect(reverse('login'))
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog=form.save(commit=False) # 디비에 저장은 안되고 폼만 만들어놓은것
            blog.author = request.user
            blog.save()
            return redirect(reverse('blog:detail', kwargs={'pk': blog.pk}))

    else:
        form = BlogForm()

    context={'form':form}
    return render(request,'blog_create.html', context)

@login_required()
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    # if request.user != blog.author:
    #     raise Http404()
    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        blog = form.save()
        return redirect(reverse('blog:detail', kwargs={'pk': blog.pk}))


    context = {'blog':blog, 'form':form}
    return render(request,'blog_update.html', context)

@login_required()
@require_http_methods(['POST']) #포스트요청만 응답하는 기능
def blog_delete(request, pk):
    # if request.method != "POST":
    #     raise Http404
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    blog.delete()
    return redirect(reverse('blog:list'))


