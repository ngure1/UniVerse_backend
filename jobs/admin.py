from django.contrib import admin
from . import models

# Register your models here.
class JobAdmin(admin.ModelAdmin):
    list_display=( "author","job_title", "job_type", "created_at","address", "application_deadline")
    search_fields = ("author", "job_title", "job_type", "application_deadline")

admin.site.register(models.Job, JobAdmin)
