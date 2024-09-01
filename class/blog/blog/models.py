from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from utils.models import TimeStampedModel

User = get_user_model()

class Blog(TimeStampedModel):
    CATEGORIES = (
        ('free','자유'),
        ('travel','여행'),
        ('cat',"고양이"),
        ('dog',"강아지")
    )
    # 카테고리

    category = models.CharField('카테고리',choices=CATEGORIES, max_length=10,default='free')
    # 제목
    title = models.CharField('제목',max_length=100)
    # 본문
    content = models.TextField('본문')
    # 작성자
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # -> 같이 삭제
    # author = models.ForeignKey(User, on_delete=models.PROTECT) -> 블로그가 있음면 유저 삭제 불가능
    # author = models.ForeignKey(User, on_delete=models.SET_NULL, null=Ture ) -> 유저 삭제시 블로그의 author가 null 이 됨

    #  => 타임스탬프로 변경
    # # 작성일자
    # created_at = models.DateTimeField('작성일자',auto_now_add=True)
    # # 수정일자
    # updated_at = models.DateTimeField('수정일자',auto_now=True)


    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'blog_pk': self.pk})

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'

 # 카테고리 업데이트
 # Blog.objects.filter(category='').update(category='free')

class Comment(TimeStampedModel):
    # blog 정보 / 블로그가 삭제되면 댓글도 필요 없기때문에 cascade
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    # 댓글 내용
    content = models.CharField('본문',max_length=255)
    # 작성자
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # =>타임스템프를 인자로 받아서 대체
    # 작성일자
    # 수정일자
    def __str__(self):
        return f'{self.blog.title} 댓글'


    class Meta:
        verbose_name = '댓글'
        verbose_name_plural='댓글 목록'
        ordering = ['-created_at']