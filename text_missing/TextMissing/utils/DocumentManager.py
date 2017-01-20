import os

from TextMissing.forms import set_file_content
from TextMissing.models import StatusChoices, Document, UploadedDocument, RectorDispositionDocument, \
    NecessityRequestDocument
from TextMissing.utils.xlsbuilder import XlsBuilder
from text_missing import settings


class  DocumentManager:
    def __init__(self):
        pass

    def __add_uploaded_document(self,document_name, author,version,abstract,keywords,status,file,size, commit=True):
        instance = UploadedDocument()
        instance.document_name = document_name
        instance.author = author
        instance.version = version
        instance.abstract = abstract
        instance.keywords = keywords
        instance.status = status
        instance.file = file
        instance.size = size
        instance.save()

    def __add_rector_disposition_document(self,document_name, author,version,abstract,keywords,status,size, commit=True):
        instance = RectorDispositionDocument()
        instance.document_name = document_name
        instance.author = author
        instance.version = version
        instance.abstract = abstract
        instance.keywords = keywords
        instance.status = status
        set_file_content(instance, instance.document_name + ".docx", self.make_doc())
        instance.size = size
        instance.save()

    def __add_necessity_request_document(self,document_name, author,version,abstract,keywords,status,user,size, commit=True):

        instance = NecessityRequestDocument()
        instance.document_name = document_name
        instance.author = author
        instance.version = version
        instance.abstract = abstract
        instance.keywords = keywords
        instance.status = status
        xl = XlsBuilder()
        xl.set_content(user)
        xl.save()
        set_file_content(instance, instance.document_name + ".xlsx", xl.file_name)
        instance.size = size
        instance.save()

    def __update_uploaded_document(self,idx,document_name,abstract,keywords,file,size,commit=True):
        instance = UploadedDocument.objects.filter(id=idx).first()
        instance.document_name = document_name
        instance.abstract = abstract
        instance.keywords = keywords
        new_file = file
        if new_file != instance.file:
            instance.file = new_file
            instance.size = size
        instance.save()

    def __update_rector_disposition_document(self,idx,document_name,abstract,keywords,size,commit=True):
            instance = RectorDispositionDocument.objects.filter(id=idx).first()
            instance.document_name = document_name
            instance.abstract = abstract
            instance.keywords = keywords
            set_file_content(instance, instance.document_name + ".docx", self.make_doc())
            instance.size = size
            instance.save()

    def __update_necessity_request_document(self, idx,document_name,abstract,keywords,user,size,commit=True):
        instance = NecessityRequestDocument.objects.filter(id=idx).first()
        instance.document_name = document_name
        instance.abstract = abstract
        instance.keywords = keywords
        xl = XlsBuilder()
        xl.set_content({"UserName": user})
        xl.save()
        set_file_content(instance, instance.document_name + ".xlsx", xl.file_name)
        instance.size = size
        instance.save()

    @staticmethod
    def remove_document(self,idx):
        files = Document.objects.filter(id=idx)
        os.remove(os.path.join(settings.MEDIA_ROOT, files.first().file.name))
        files.delete()
