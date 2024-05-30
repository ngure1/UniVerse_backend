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
    list_display = ('user_first_name', 'user_last_name', 'created_at')
    search_fields = ('user_first_name', 'user_last_name')

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'First Name'

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = 'Last Name'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('owner','street', 'city', 'postal_code', 'country')
    search_fields = ('country', 'city', 'street')

class EducationAdmin(admin.ModelAdmin):
    list_display = ('owner','institution_name', 'field_of_study', 'start_date', 'end_date')
    search_fields = ('institution_name', 'field_of_study')

# Register your models here.
admin.site.register(models.MyUser, MyUserAdmin)
admin.site.register(models.UserProfile, MyUserProfileAdmin)
admin.site.register(models.Education, EducationAdmin)
admin.site.register(models.Address, AddressAdmin)
