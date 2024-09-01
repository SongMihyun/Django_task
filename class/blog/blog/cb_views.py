from IPython.extensions.autoreload import UPDATE_RULES
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from blog.forms import CommentForm
from blog.models import Blog, Comment


class BlogListView(ListView):
    # model = Blog # =>queryset = Blog.objects.all() 과 같음
    # queryset = Blog.objects.all().order_by('-created_at')#  정렬이 필요할경우1
    queryset = Blog.objects.all()   #model=Blog 와 같음
    ordering = ('-created_at',)     #정렬이 필요할경우2
    template_name = 'blog_list.html'
    paginate_by = 10        #페이지네이션 한줄로 끝

    # 리스트뷰에 내장되어있는 함수
    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q')
        if q :
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )
        return queryset


class BlogDetailView(ListView):
    model = Comment
    # queryset = Blog.objects.all().prefetch_related('comment_set','comment_set__author')
    template_name = 'blog.html'
    paginate_by = 20

    def get(self,request,*args,**kwargs):
        self.object = get_object_or_404(Blog,pk=kwargs.get('blog_pk'))
        return super().get(request,*args,**kwargs)

    def get_queryset(self):
        return self.model.objects.filter(blog=self.object).prefetch_related('author')

    #전체 쿼리셋에 대한 내용 .?
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(id__lte=50) #50이하만 불러올수 있게..

    # # 필터링된 한개의 개체를 가져올때
    # def get_object(self, queryset=None):
    #     object = super().get_object()       #한개체만 가져올때 오브젝트사용
    #     # object = self.model.objects.get(pk=self.kwargs.get('pk'))
    #     return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['blog'] = self.object
        return context

    # def post(self,*args, **kwargs):
    #     comment_form = CommentForm(self.request.POST)
    #     if not comment_form.is_valid():
    #         self.object = self.get_object()
    #         context = self.get_context_data(object=self.object)
    #         context['comment_form'] = comment_form
    #         return self.render_to_response(context)
    #
    #     if not self.request.user.is_authenticated:
    #         raise Http404
    #     comment=comment_form.save(commit=False)
    #     # comment.blog=self.get_object()
    #     comment.blog_id = self.kwargs['pk'] #url에서 가져오는것임
    #     comment.author = self.request.user
    #     comment.save()
    #
    #     return HttpResponseRedirect(reverse_lazy('blog:detail',kwargs={'pk':self.kwargs['pk']}))
    # #


class BlogCreateView(LoginRequiredMixin,CreateView):
    model = Blog
    template_name = 'blog_form.html'
    fields = ('category','title', 'content')
    # success_url = reverse_lazy('cb_blog_list') # 정적인url을 이용할때는 이용해도 무방

    def form_valid(self, form):
        self.object = form.save(commit=False) #커밋펄스는 디비에 저장이 되지 않는걸 의미
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title']='작성'
        context['btn_name']='생성'
        return context


    # 동적인 url을 사용하려면 get_success_url을 이용하는게 좋다.
    def get_success_url(self):
        return reverse_lazy('blog:detail',kwargs={'pk':self.object.pk})


class BlogUpdateView(LoginRequiredMixin,UpdateView):
    model = Blog
    template_name = 'blog_form.html'
    fields = ('category','title', 'content')

    # get_success_url 가 없으면 get_absolute_url을 찾아서 알아서 실행함
    # def get_success_url(self):
    #     return reverse_lazy('cb_blog_detail',kwargs={'pk':self.object.pk})


    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title']='수정'
        context['btn_name']='수정'
        return context

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #
    #     if self.object.author != self.request.user:
    #         raise Http404
    #     return self.object


class BlogDeleteView(LoginRequiredMixin,DeleteView):
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(author=self.request.user)
        return queryset



    def get_success_url(self):
        return reverse_lazy('blog:list')


class CommentCreateView(LoginRequiredMixin,CreateView):
    model = Comment
    form_class = CommentForm

    def get(self, *args, **kwargs):
        raise Http404



    def form_valid(self, form):
        blog=self.get_blog()
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.blog = self.get_blog()
        self.object.save()

        return HttpResponseRedirect(reverse('blog:detail',kwargs={'blog_pk':blog.pk}))

    def get_blog(self):
        pk = self.kwargs['blog_pk']
        blog = get_object_or_404(Blog, pk=pk)
        return blog

    # /comment/create/<int:blog_pk>/