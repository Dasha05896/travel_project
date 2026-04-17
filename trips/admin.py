from django.contrib import admin
from .models import TravelProject, Place


@admin.register(TravelProject)
class TravelProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_completed", "start_date")


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("id", "external_id", "project", "is_visited")
