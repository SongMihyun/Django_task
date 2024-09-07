from django import forms
from .models import Todo, Comment


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'description','start_date','end_date')



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ['content']
        exclude = ['todo','author'] # 폼에서 todo 필드를 제외

        widgets = {'content': forms.Textarea(
            attrs={
                'placeholder': '댓글을 작성하세요.',
                'style': 'width: 100%; height: 30px; display: flex; border: 0; line-height: 30px;',
                })}
        labels = {'content':''}

    def __init__(self, *args, **kwargs):
        self.todo = kwargs.pop('todo',None)
        super(CommentForm, self).__init__(*args, **kwargs)


    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.todo:
            instance.todo = self.todo
        if commit:
            instance.save()
        return instance