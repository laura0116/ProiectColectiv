from django.contrib import admin


# Register your models here.
from TextMissing.models import Document, DocumentFlow


class DocumentAdmin(admin.ModelAdmin):

    fields = ['document_name', 'author', 'version', 'flow', 'abstract', 'keywords', 'status', 'file']
    list_display = ['document_name', 'author', 'flow', 'size', 'version', 'abstract', 'keywords', 'status', 'file']



class DocumentFlowAdmin(admin.ModelAdmin):
    fields = ['name', 'flow_type', 'initiator', 'state']
    list_display = ['name', 'flow_type', 'initiator', 'state', 'documents_in_flow']

#admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentFlow, DocumentFlowAdmin)
