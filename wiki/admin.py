from django.contrib import admin
from .models import Wiki

# Register your models here.


@admin.register(Wiki)
class WikiAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "get_title_id",
    )

    # list_filter = ("category",)
    def get_title_id(self, obj):
        return "\n".join([p.title_id for p in obj.title_id.all()])
