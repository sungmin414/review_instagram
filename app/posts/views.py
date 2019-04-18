from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# from members.models import User
from .forms import PostCreateForm
from .models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/post_list.html', context)


@login_required
def post_create(request):
    if not request.user.is_authenticated:
        return redirect('members:login')

    context = {}
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(author=request.user)
            return redirect('posts:post-list')
    else:
        # GET요청의 경우, 빈 Form인스턴스를 context에 담아서 전달
        # Template에서는 'form'키로 해당 Form인스턴스 속성을 사용 가능
        form = PostCreateForm()

    context['form'] = form
    return render(request, 'posts/post_create.html', context)
