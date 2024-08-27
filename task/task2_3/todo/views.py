

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Todo
from .forms import TodoForm


@login_required(login_url='login')
def todo_list(request):
    todo_list = Todo.objects.all()

    # 페이지네이션
    paginator = Paginator(todo_list, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)


    form = TodoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse('todo_list'))

    context = {'form': form, 'page_obj': page_obj}
    return render(request, 'todo_list.html', context)


@login_required(login_url='login')
def todo_info(request,pk):
    todo = Todo.objects.get(id = pk)
    edit_form = TodoForm(request.POST,instance=todo or None)
    if edit_form.is_valid():
        edit_form.save()
        return redirect(reverse('todo_info',args=[pk]))
    edit_form = TodoForm(instance=todo)
    context = {'todo':todo ,'edit_form':edit_form }
    return render(request,'todo_info.html',context)

@login_required(login_url='login')
def todo_delete(request,pk):
    todo = get_object_or_404(Todo, id=pk)
    todo.delete()
    return redirect('todo_list')









