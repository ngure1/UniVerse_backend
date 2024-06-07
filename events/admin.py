from django.contrib import admin
from . import models


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ("creator","title","created_at","address","capacity")
    search_fields = ("creator","title","created_at","address","capacity")  

admin.site.register(models.Event,EventAdmin)

