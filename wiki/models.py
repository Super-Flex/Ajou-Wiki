from django.db import models
from common.models import CommonModel


# Create your models here.
class Wiki(CommonModel):

    """Wiki Model Definition"""

    name = models.CharField(
        max_length=30,
        default="",
    )

    title_id = models.ManyToManyField(
        "wiki_detail.Wiki_Detail",
        null=True,
        blank=True,
        related_name="wiki_detail",
    )

    # tag_id = models.ManyToManyField(
    #     "rooms.Amenity",
    #     related_name="tag_id",
    # )
    def __str__(self) -> str:
        return self.name
    