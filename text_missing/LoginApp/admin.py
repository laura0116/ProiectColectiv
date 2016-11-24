from django.contrib import admin


# Register your models here.
# TODO: Register different types of users
from LoginApp.models import Contributor


class ContributorAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name']
    list_display = ['get_user', 'last_name', 'first_name', 'email', 'is_activated', 'get_temp_pass']


admin.site.register(Contributor, ContributorAdmin)