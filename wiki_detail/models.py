from django.db import models
from common.models import CommonModel


# Create your models here.
class Wiki_Detail(CommonModel):

    """Wiki_Detail Model Definition"""

    title = models.CharField(
        max_length=30,
        default="",
    )

    wiki_id = models.ForeignKey(
        "wiki.Wiki",
        on_delete=models.CASCADE,
        related_name="wiki_id",
    )

    order = models.IntegerField()
    description = models.CharField(
        max_length=3000,
        blank=True,
        null=True,
    )
    user_id = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="user",
    )

    def __str__(self) -> str:
        return self.title
