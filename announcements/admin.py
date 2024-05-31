# announcements/admin.py
from django.contrib import admin
from .models import Announcement

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'created_at')
    search_fields = ('title', 'creator__user__username', 'content')

admin.site.register(Announcement, AnnouncementAdmin)
