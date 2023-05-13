from django.db import models

# Create your models here.
class CommonModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,  # 만들어진 시간
    )
    updated_at = models.DateTimeField(
        auto_now=True,  # 마지막으로 저장된 시간
    )

    class Meta:
        abstract = True
