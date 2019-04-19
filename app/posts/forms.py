from django import forms

from .models import Post


class PostCreateForm(forms.Form):
    photo = forms.ImageField(
        widget=forms.FileInput(
            # HTML위젯의 속성 설정
            # form-control-file클래스를 사
            attrs={
                'class': 'form-control-file',
            }
        )
    )
    comment = forms.CharField(
        # 반드시 채워져 있을 필요는 없음
        required=False,
        # HTML렌더링 위젯으로 textarea를 사용
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def save(self, **kwargs):
        post = Post.objects.create(
            photo=self.cleaned_data['photo'],
            **kwargs,
        )
        comment_content = self.cleaned_data.get('comment')
        if comment_content:
            post.comments.create(
                author=post.author,
                content=comment_content,
            )

        return post
