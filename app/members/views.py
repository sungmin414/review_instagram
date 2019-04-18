from django.contrib.auth import authenticate, login, logout
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
    if request.method == 'POST':
        pass
    else:
        form = SignupForm()
        context = {
            'form': form
        }
        return render(request, 'members/signup.html', context)
