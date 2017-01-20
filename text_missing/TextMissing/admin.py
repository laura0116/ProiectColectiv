from django.contrib import admin


# Register your models here.
from TextMissing.models import Document


class DocumentAdmin(admin.ModelAdmin):
    fields = ['document_name', 'author', 'version', 'abstract', 'keywords', 'status', 'file']
    list_display = ['document_name', 'author', 'size', 'version', 'abstract', 'keywords', 'status', 'file']

admin.site.register(Document, DocumentAdmin)

