from django.contrib import admin
from . import models


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ("author","title","created_at", "capacity")
    search_fields = ("author","title","created_at", "capacity")

admin.site.register(models.Event,EventAdmin)

