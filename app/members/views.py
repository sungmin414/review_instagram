from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import LoginForm, SignupForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            # 인증성공시
            login(request, user)
            return redirect('posts:post-list')
        else:
            # 인증실패시
            pass

    else:
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'members/login.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('posts:post-list')


def signup_view(request):
    context = {
        'form': SignupForm,
    }
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            context['error'] = f'({username})은 이미 사용중입니다'
        elif password1 != password2:
            context['error'] = '비밀번호와 비밀번호 확인란의 값이 일치하지 않습니다'
        else:
            # create_user메서드는 create와 달리 자동으로 password해싱을 해줌
            user = User.objects.create_user(
                username=username,
                password=password1,
            )
            login(request, user)
            return redirect('posts:post-list')
    return render(request, 'members/signup.html', context)
