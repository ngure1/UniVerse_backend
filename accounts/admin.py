from django.contrib import admin
from .import models

class MyUserAdmin(admin.ModelAdmin):
    list_display=("first_name", "last_name", "email")
class MyUserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_first_name', 'user_last_name', 'created_at')

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'First Name'

    def user_last_name(self, obj):
        return obj.user.last_name
    user_last_name.short_description = 'Last Name'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user')
        return queryset
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user_first_name', 'user_last_name', 'county')

    def user_first_name(self, obj):
        return obj.userprofile.user.first_name if obj.userprofile else None
    user_first_name.short_description = 'First Name'

    def user_last_name(self, obj):
        return obj.userprofile.user.last_name if obj.userprofile else None
    user_last_name.short_description = 'Last Name'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('userprofile__user')  # Optimizes the query to include related user data
        return queryset

class EducationAdmin(admin.ModelAdmin):
    list_display = ('user_first_name', 'user_last_name', 'institution_name', 'field_of_study')

    def user_first_name(self, obj):
        return obj.userprofile.user.first_name if obj.userprofile else None
    user_first_name.short_description = 'First Name'

    def user_last_name(self, obj):
        return obj.userprofile.user.last_name if obj.userprofile else None
    user_last_name.short_description = 'Last Name'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('userprofile__user')  # Optimizes the query to include related user data
        return queryset

admin.site.register(models.MyUser, MyUserAdmin)
admin.site.register(models.UserProfile, MyUserProfileAdmin)
admin.site.register(models.Education, EducationAdmin)
admin.site.register(models.Address, AddressAdmin)