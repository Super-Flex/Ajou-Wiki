# Register your models here.
from django.contrib import admin
from .models import Wiki_Detail


@admin.register(Wiki_Detail)
class WikiDetailAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "wiki_id",
        "order",
        "description",
        "user_id",
        "created_at",
        "updated_at",
    )
    # list_filter = ("category",)
