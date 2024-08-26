from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from todo.models import Todo


@login_required(login_url='login')
def todo_list(request):
    todo_list = Todo.objects.all()
    context = {'todo_list':todo_list}
    return render(request,'todo_list.html',context)

@login_required(login_url='login')
def todo_info(request,pk):
    todo = Todo.objects.filter(id = pk)

    context = {'todo':todo}
    return render(request,'todo_info.html',context)