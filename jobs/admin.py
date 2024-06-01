from django.contrib import admin
from . import models

# Register your models here.
class JobAdmin(admin.ModelAdmin):
    list_display=( "job_owner","title", "description", "created_at", "application_deadline")
    search_fields = ("job_owner", "title", "description", "application_deadline")

admin.site.register(models.Job, JobAdmin)
