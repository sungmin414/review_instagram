from django.shortcuts import render

from .forms import LoginForm


def login_view(request):
    if request.method == 'POST':
        pass
    else:
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'members/login.html', context)
