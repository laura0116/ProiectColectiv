from django.contrib import admin


# Register your models here.
from LoginApp.models import Contributor, Manager, Reader, Staff, UserGroup, GroupType


class ContributorAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email']
    list_display = ['get_user', 'last_name', 'first_name', 'email', 'is_activated', 'get_temp_pass']

class ManagerAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email']
    list_display = ['get_user', 'last_name', 'first_name', 'email', 'is_activated', 'get_temp_pass']


class ReaderAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email']
    list_display = ['get_user', 'last_name', 'first_name', 'email', 'is_activated', 'get_temp_pass']


class StaffAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'email']
    list_display = ['get_user', 'last_name', 'first_name', 'email', 'is_activated', 'get_temp_pass']


class UserGroupAdmin(admin.ModelAdmin):
    fields = ['name', 'leader', 'users', 'type']
    list_display = ['get_usergroup', 'get_leader', 'get_users']
    list_filter = ('type',)


class GroupTypeAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['type_name', 'user_groups']

admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(UserGroup, UserGroupAdmin)
admin.site.register(GroupType, GroupTypeAdmin)