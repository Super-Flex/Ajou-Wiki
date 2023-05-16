from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    class SexKindChoices(models.TextChoices):
        MAN = "man", "남자"
        WOMAN = "woman", "여자"

    name = models.CharField(
        max_length=30,
        default="",
    )

    department = models.CharField(
        max_length=30,
        default="",
    )

    sex = models.CharField(
        max_length=10,
        null=True,
        choices=SexKindChoices.choices,
    )

    email = models.EmailField(
        max_length=30,
    )

    student_id = models.TextField(
        unique=True,
        default=0
    )