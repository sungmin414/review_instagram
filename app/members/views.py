from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import LoginForm, SignupForm


def login_view(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            # GET parameter에 'next'가 전달되었다면
            # 해당 키의 값으로 redirect
            next_path = request.GET.get('next')
            if next_path:
                return redirect(next_path)
            return redirect('posts:post-list')

    else:
        form = LoginForm()

    context['form'] = form
    return render(request, 'members/login.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('posts:post-list')


def signup_view(request):
    context = {}
    if request.method == 'POST':
        # POST로 전달된 데이터를 확인
        # 올바르다면 User를 생성하고 post-list화면으로 이동
        # (is_valid()가 True면 올바르다고 가정)
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # form이 유효하면 여기서 함수 실행 종료
            return redirect('posts:post-list')
        # form이 유효하지 않을 경우, 데이터가 바인딩된 상태로 if-else구문 아래의 render까지 이동
    else:
        # GET요청시 빈 Form을 생성
        form = SignupForm()
    # GET 요청시 또는 POST로 전달된 데이터가 올바르지 않을 경우
    # signup.html에 빈 Form또는 올바르지 않은 데이터에 대한 정보가 포함된 Form을 전달해서
    # 동적으 form을 렌더링
    context['form'] = form
    return render(request, 'members/signup.html', context)
