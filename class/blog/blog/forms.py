from django import forms

from blog.models import Blog, Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        # fields = '__all__' # 전체를 적용하고 싶을때
        fields = ('title','content')    #리스트, 튜플 로 원하는 컬럼명을 적어주면 됨

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)  #튜플이기때문에 하나만있어도 컴마 꼭 찍어야 함
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'content':'댓글'
        }
