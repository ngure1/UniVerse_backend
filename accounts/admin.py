from django.contrib import admin
from . import models

admin.site.site_header = "UniVerse Admin"
admin.site.site_title = "UniVerse Admin Area"
admin.site.index_title = "Welcome to the UniVerse Admin Area"

# List dsplay for UniVerse_Account_Admin
class MyUserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")
    search_fields = ('first_name', 'last_name')

class MyUserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user_first_name', 'user_last_name', 'address', 'user_email', 'created_at')
    search_fields = ('user_first_name', 'user_last_name', 'user_email')
    list_filter = ('user__is_active', 'created_at', 'updated_at')

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'First Name'

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = 'Last Name'

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

    def is_active(self, obj):
        return obj.user.is_active
    is_active.short_description = 'Active'
    is_active.boolean = True

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'city', 'postal_code', 'country')
    search_fields = ('country', 'city', 'street')

class EducationAdmin(admin.ModelAdmin):
    list_display = ('owner','institution_name', 'field_of_study', 'start_date', 'end_date')
    search_fields = ('institution_name', 'field_of_study')

class FollowerAdmin(admin.ModelAdmin):
    list_display = ('id','follower', 'followed', 'created_at' )
    search_fields = ('follower_name', 'followed_name')

    # Define methods to display follower's and followed person's full name and email
    def follower_name(self, obj):
        return f"{obj.follower.user.first_name} {obj.follower.user.last_name}"
    follower_name.short_description = 'Follower Name'
    
    def followed_name(self, obj):
        return f"{obj.followed.user.first_name} {obj.followed.user.last_name}"
    followed_name.short_description = 'Followed Name'

# Register your models here.
admin.site.register(models.MyUser, MyUserAdmin)
admin.site.register(models.UserProfile, MyUserProfileAdmin)
admin.site.register(models.Education, EducationAdmin)
admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.Follower, FollowerAdmin)
