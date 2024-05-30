from django.contrib import admin
from . import models

admin.site.site_header = "UniVerse Admin"
admin.site.site_title = "UniVerse Admin Area"
admin.site.index_title = "Welcome to the UniVerse Admin Area"

# Register your models here.
class SupportAdmin(admin.ModelAdmin):
    list_display=( "title", "description", "created_at", "amount")
    search_fields = ('title', 'description', 'amount')


admin.site.register(models.Support, SupportAdmin)