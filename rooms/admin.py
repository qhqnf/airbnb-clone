from django.contrib import admin
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class RoomType(admin.ModelAdmin):

    """ Item Admin Definition """

    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "description", "country", "address", "price",)},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book",)},),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "More about spaces",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilities", "house_rules",),
            },
        ),
        ("Last details", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
    )

    list_filter = (
        "instant_book",
        "city",
        "country",
        "roomtype",
        "amenities",
        "facilities",
        "house_rules",
    )

    filter_horizontal = ("amenities", "facilities", "house_rules")

    search_fields = ("^city", "^host__username")

    def count_amenities(self, obj):
        print(obj.amenities.all())
        return "Potato"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    pass
