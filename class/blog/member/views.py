
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.conf import settings #장고가 실행되고 있는 환경에 settings파일을 찾아옴 / 이름이 바뀌어도 오류가 안남
# from config import settings  -> 이름이 바뀌면 오류가 날수 있음 / 비추
from django.contrib.auth import login as django_login

def sign_up(request):
    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    # username 중복확인작업
    # 패스워드가 맞는지, 그리고 패스워드 정책에 올바른지(대소문자)

    # if request.method == 'POST':    #POST요청일때
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid(): #유저 정책에 올바르면
    #         form.save()     #디비에 저장
    #         return redirect('/accounts/login/')
    # else:
    #     # GET요청일때
    #     form = UserCreationForm() #장고에서 지원하는 기본 폼

    # 폼에 POST데이터가 있으면 넣고, 없으면 아무것도 넣지 말아라
    form = UserCreationForm(request.POST or None)
    if form.is_valid():     #None일경우 벨리드할수없음. 그러니 그냥 넘어가짐
        form.save()         #POST가 들어가면 벨리드 한지 확인후 디비 저장
        # return redirect('/accounts/login/') #주소 설정이 고정적이라서 비추천
        return redirect(settings.LOGIN_URL)
    context = {'form': form}
    # POST요청이 들어갔지만 if의 벨리드하지 않다면 아래 리턴 실행
    return render(request, 'registration/sign_up.html', context)

def login(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        django_login(request, form.get_user())

        next =request.GET.get('next')
        if next:
            return redirect(next)

        return redirect(reverse('blog:list'))   #리버스 -> 이름으로 path찾음

    context = {'form':form}
    return render(request, 'registration/login.html', context)


