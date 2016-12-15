from django.contrib import admin


# Register your models here.
from LoginApp.models import Contributor, Manager, Reader, Staff


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


admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Reader, ReaderAdmin)
admin.site.register(Staff, StaffAdmin)