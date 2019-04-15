from django.shortcuts import render
from .models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/post_list.html', context)


def post_create(request):
    # posts = Post.objects.create()
    # context = {
    #     'posts': posts
    # }
    return render(request, 'posts/post_create.html')