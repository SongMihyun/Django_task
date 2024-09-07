from django.contrib.auth import get_user_model
from django.db import models
from utils.models import TimeStampModel


User = get_user_model()
class Todo(TimeStampModel):
    title=models.CharField(max_length=50)
    description=models.TextField()
    start_date=models.DateField()
    end_date=models.DateField()
    is_completed=models.BooleanField(default=False)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    # created_at=models.DateTimeField(auto_now_add=True)
    # updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}, {self.description}, {self.start_date}, {self.end_date}'

    class Meta:
        verbose_name="Todo"
        verbose_name_plural='Todo List'


class Comment(TimeStampModel):
    # 투두 /해당 투두가 삭제되면 댓글도 함께 삭제
    todo = models.ForeignKey(Todo,on_delete=models.CASCADE)
    # 댓글 내용
    content=models.TextField()
    # 작성자
    author =models.ForeignKey(User,on_delete=models.CASCADE)
    # created_at=models.DateTimeField(auto_now_add=True)
    # updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.content}'

    class Meta:
        verbose_name='댓글'
        verbose_name_plural='댓글 목록'
        ordering=['-created_at']