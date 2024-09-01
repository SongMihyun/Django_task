from django.db import models


class TimeStampedModel(models.Model):
    # 작성일자
    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    # 수정일자
    updated_at = models.DateTimeField('수정일자', auto_now=True)

    class Meta:
        abstract = True    #상속을 할거고 실제로 디비에서 사용할게 아니므로 abstract를 사용