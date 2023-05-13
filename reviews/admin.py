from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):

    title = "Filter by words!"

    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),  # (Url, filter)
        ]

    def queryset(self, request, reviews):
        word = self.value()  # url의 vaule값을 가져옴 good, great, awersome
        if word:
            return reviews.filter(payload__contains=word)
        else:
            return reviews


class PNFilter(admin.SimpleListFilter):

    title = "Filter by P/N!"

    parameter_name = "P_N"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),  # (url, admin fillter에 표시)
            ("bad", "Bad"),
        ]

    def queryset(self, request, reviews):
        rate = self.value()
        if rate == "good":
            return reviews.filter(rating__gte=3)
        elif rate == "bad":
            return reviews.filter(rating__lt=3)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "payload",
    )

    list_filter = (
        WordFilter,
        PNFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )
