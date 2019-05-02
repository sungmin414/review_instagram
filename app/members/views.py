import imghdr
import io
import json
from pprint import pprint

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import LoginForm, SignupForm, UserProfileForm

User = get_user_model()


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


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=request.user)
        if form.is_valid():
            form.save()

            # messages.add_message(request, messages.SUCCESS, '프로필 수정이 완료되었습니다.',)
            messages.success(request, '프로필 수정이 완료되었습니다.')

    form = UserProfileForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'members/profile.html', context)


def facebook_login(request):
    api_base = 'https://graph.facebook.com/v3.2'
    api_get_access_token = f'{api_base}/oauth/access_token?'
    api_me = f'{api_base}/me'
    # 페이스북으로부터 받아온 request token
    code = request.GET.get('code')

    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': 'http://localhost:8000/members/facebook-login/',
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'code': code,
    }
    # request token을 access token으로 교환
    response = requests.get(api_get_access_token, params)
    # 인수로 전달한 문자열이 'JSON' 형식일 것으로 생각
    # json.loads는 전달한 문자열이 JSON형식일 경우, 해당 문자열을 parsing해서 파이썬 Object를 리턴함
    # response_object = json.loads(response.text)

    data = response.json()
    access_token = data['access_token']

    # access_token을 사용해서 사용자 정보를 가져오기
    params = {
        'access_token': access_token,
        'fields': ','.join([
            'id',
            'first_name',
            'last_name',
            'picture.type(large)',
        ]),
    }
    response = requests.get(api_me, params)
    data = response.json()
    facebook_id = data['id']
    first_name = data['first_name']
    last_name = data['last_name']
    url_img_profile = data['picture']['data']['url']
    # HTTP GET요청의 응답을 받아와서 binary data를 img_data변수에 할당
    img_response = requests.get(url_img_profile)
    img_data = img_response.content

    # 응답의 binary data를 사용해서 In-memory binary stream(file)객체를 생성
    # 이렇게 안하고 FileField 가 지원하는 InMemoryUploadedFile 객체를 사용하기!
    # f = io.BytesIO(img_response.content)

    # imghdr 모듈을 사용해 image binary data 의 확장자를 알아냄
    ext = imghdr.what('', h=img_data)
    # Form에서 업로드한 것과 같은 형태의 file-like object 생성
    # 첫 번째 인수로 반드시 파일며잉 필요. <facebook_id>.<확장자> 형태의 파일명을 지
    f = SimpleUploadedFile(f'{facebook_id}.{ext}', img_response.content)

    try:
        user = User.objects.get(username=facebook_id)
        # update_or_create
        user.last_name = last_name
        user.first_name = first_name
        # user.img_profile = f
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=facebook_id,
            first_name=first_name,
            last_name=last_name,
            img_profile=f,
        )
    login(request, user)
    return redirect('posts:post-list')

