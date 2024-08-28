from IPython.extensions.autoreload import UPDATE_RULES
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from blog.models import Blog


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


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog.html'

    #전체 쿼리셋에 대한 내용 .?
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(id__lte=50) #50이하만 불러올수 있게..

    # # 필터링된 한개의 개체를 가져올때
    # def get_object(self, queryset=None):
    #     object = super().get_object()       #한개체만 가져올때 오브젝트사용
    #     # object = self.model.objects.get(pk=self.kwargs.get('pk'))
    #     return object

    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['test'] = 'test'
    #     return context


class BlogCreateView(LoginRequiredMixin,CreateView):
    model = Blog
    template_name = 'blog_create.html'
    fields = ('category','title', 'content')
    # success_url = reverse_lazy('cb_blog_list') # 정적인url을 이용할때는 이용해도 무방

    def form_valid(self, form):
        self.object = form.save(commit=False) #커밋펄스는 디비에 저장이 되지 않는걸 의미
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # 동적인 url을 사용하려면 get_success_url을 이용하는게 좋다.
    def get_success_url(self):
        return reverse_lazy('blog:detail',kwargs={'pk':self.object.pk})


class BlogUpdateView(LoginRequiredMixin,UpdateView):
    model = Blog
    template_name = 'blog_update.html'
    fields = ('category','title', 'content')

    # get_success_url 가 없으면 get_absolute_url을 찾아서 알아서 실행함
    # def get_success_url(self):
    #     return reverse_lazy('cb_blog_detail',kwargs={'pk':self.object.pk})


    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user)

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