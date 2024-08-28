from urllib import request

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from todo.forms import TodoForm
from todo.models import Todo
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




class TodoDetailView(LoginRequiredMixin,DetailView):
    model = Todo
    template_name = 'todo_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TodoForm()
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

