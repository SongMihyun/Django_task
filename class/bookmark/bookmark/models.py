from django.db import models


# Model = DB의 테이블
# Field = DB의 칼럼

# 북마크
# 이름 ==> varchar
# URL 주소 ==> varchar
class Bookmark(models.Model):
    name = models.CharField('이름',max_length=100)
    url = models.URLField('URL')
    created_at = models.DateTimeField('생성일시',auto_now_add=True)
    updated_at = models.DateTimeField('수정일시',auto_now = True)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name='북마크'
        verbose_name_plural='북마크 목록'

# python manage.py makemigration
# makemigrations => migration.py 파일을 만듭니다.
# 실제 디비에는 영향이 없다 => 실제 디비에 넣기위한 정의를 하는 파일을 생성

# python manage.py migrate
# migrate => migrations/ 폴더 안에 있는 migration 파일들을 실제  DB에 적용을 합니다.

# makemigrations => git의 커밋과 비슷 -> 깃허브에 적용은 안됨 ,커밋 기록 -> 디비에 적용안됨, 대신 적용할 파일을 만듬, 생성됨
#  migrate => git의 push 랑 미슷 -> 깃허브에 적용이 됨 , 로컬에 있는 커밋기록을 사용-> 디비에 적용됨, migrations 파일을 가지고 적용


