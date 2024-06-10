from django.contrib import admin
from . import models

# Register your models here.
class JobAdmin(admin.ModelAdmin):
    list_display=( "author","title", "description", "created_at", "application_deadline")
    search_fields = ("author", "title", "description", "application_deadline")

admin.site.register(models.Job, JobAdmin)
