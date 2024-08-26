from django.http import HttpResponse
from django.shortcuts import render

from todo.models import Todo


def index(request):
    return HttpResponse("hello world")

def todo_list(request):
    todo_list = Todo.objects.all()
    context = {'todo_list':todo_list}
    return render(request,'todo_list.html',context)


def todo_info(request,pk):
    todo = Todo.objects.filter(id = pk)

    context = {'todo':todo}
    return render(request,'todo_info.html',context)