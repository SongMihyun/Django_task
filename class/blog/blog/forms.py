from django import forms

from blog.models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        # fields = '__all__' # 전체를 적용하고 싶을때
        fields = ('title','content')    #리스트, 튜플 로 원하는 컬럼명을 적어주면 됨