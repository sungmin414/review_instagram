import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# from members.models import User
from .forms import PostCreateForm, CommentCreateForm, CommentForm, PostForm
from .models import Post, Comment, HashTag


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
        'comment_form': CommentForm(),
    }
    return render(request, 'posts/post_list.html', context)


@login_required
def post_create(request):
    context = {}
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            comment_content = form.cleaned_data['comment']
            # 위에서 생성한 Post에 연결되는 Comment생성
            if comment_content:
                post.comments.create(
                    author=request.user,
                    content=comment_content,
                )
            return redirect('posts:post-list')
    else:
        # GET요청의 경우, 빈 Form인스턴스를 context에 담아서 전달
        # Template에서는 'form'키로 해당 Form인스턴스 속성을 사용 가능
        form = PostForm()

    context['form'] = form
    return render(request, 'posts/post_create.html', context)


def comment_create(request, post_pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect('posts:post-list')


def tag_post_list(request, tag_name):
    # Post중, 자신에게 속한 Comment가 가진 HashTag목록 중
    # Post목록을 posts변수에 할당
    # context에 담아서 리턴 render
    # HTML: /posts/tag_post_list.html
    posts = Post.objects.filter(comments__tags__name=tag_name)
    context = {
        'posts': posts
    }
    return render(request, 'posts/tag_post_list.html', context)


def tag_search(request):
    # request.GET으로 전달된
    # search_keyword값을 적절히 활용해서
    # 위의 tag_post_list view로 redirect
    # URL: 'posts/tag-search/'
    # URL Name : 'posts:tag-search'
    # Template: 없
    search_keyword = request.GET.get('search_keyword')
    substituted_keyword = re.sub(r'#|\s+', '', search_keyword)
    return redirect('tag-post-list', substituted_keyword)
