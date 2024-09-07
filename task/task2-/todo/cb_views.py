
from urllib import request

from IPython.core.page import pager_page
from django.contrib.admin.templatetags.admin_list import paginator_number
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import success
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from todo.forms import TodoForm, CommentForm
from todo.models import Todo, Comment
from todo.views import todo_list


class TodoListView(LoginRequiredMixin, ListView):
    model  = Todo
    template_name = 'todo_list.html'
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TodoForm()
        return context


class TodoCreateView(LoginRequiredMixin,CreateView):
    model = Todo
    template_name = 'todo_create.html'
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save(commit=False)  # 커밋펄스는 디비에 저장이 되지 않는걸 의미
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

        # 동적인 url을 사용하려면 get_success_url을 이용하는게 좋다.

    def get_success_url(self):
        return reverse_lazy('todo:info', kwargs={'pk': self.object.pk})




class TodoDetailView(LoginRequiredMixin,ListView):
    model = Comment
    template_name = 'todo_info.html'
    paginate_by = 10

    def get(self,request,*args,**kwargs):
        self.object = get_object_or_404(Todo,pk=kwargs.get('todo_pk'))
        return super().get(request,*args,**kwargs)

    def get_queryset(self):
        return self.model.objects.filter(todo=self.object).prefetch_related('todo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo'] = self.object
        context['comment_form'] = CommentForm()
        return context



class TodoDeleteView(LoginRequiredMixin,DeleteView):
    model = Todo

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('todo:list')


class TodoUpdateView(LoginRequiredMixin,UpdateView):
    model = Todo
    template_name = 'todo_update.html'
    fields = ('__all__')


    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user)


    def get_success_url(self):
        return reverse_lazy('todo:info', kwargs={'pk': self.object.pk})




class CommentCreateView(LoginRequiredMixin,CreateView):
    model = Comment
    form_class = CommentForm

    def get(self,*args, **kwargs):
        raise Http404

    def get_todo(self):
        return get_object_or_404(Todo,pk=self.kwargs['todo_pk'])

    def form_valid(self, form):
        todo = self.get_todo()
        self.object = form.save(commit=False)
        self.object.author = self.request.user  # 로그인한 사용자를 작성자로 설정
        self.object.todo = todo     # Todo 객체를 Comment에 연결
        self.object.save()
        return HttpResponseRedirect(reverse('todo:info',kwargs={'todo_pk':todo.pk}))

class CommentDeleteView(LoginRequiredMixin,DeleteView):
    model = Comment
    def get_queryset(self):
        queryset = super().get_queryset()
        page = self.request.GET.get('page')
        if not self.request.user.is_superuser:
            queryset = queryset.filter(author=self.request.user)

        print(page)
        return queryset

    def get_success_url(self):
        todo = self.object.todo
        page = self.request.GET.get('page')
        success_url = reverse('todo:info', kwargs={'todo_pk': todo.pk}) + f'?page={page}'

        return success_url