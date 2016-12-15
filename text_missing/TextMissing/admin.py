from django.contrib import admin


# Register your models here.
from TextMissing.models import Document


class DocumentAdmin(admin.ModelAdmin):
    fields = ['document_name', 'author', 'version', 'creation_date', 'last_update', 'abstract', 'keywords', 'status']
    list_display = ['document_name', 'author', 'size', 'version', 'abstract', 'keywords', 'status']

admin.site.register(Document, DocumentAdmin)

