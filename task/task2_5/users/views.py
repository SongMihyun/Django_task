

from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse

def login(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        django_login(request, form.get_user())

        next = request.GET.get('next')
        if next:
            return redirect(next)

        return redirect(reverse('todo:list'))



    context={'form':form}
    return render(request,'registration/login.html',context)

def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse('todo:list'))
    context = {'form':form}
    return render(request, 'registration/sign_up.html', context)
