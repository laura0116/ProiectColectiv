import os

from TextMissing.forms import *
from TextMissing.models import StatusChoices, Document, UploadedDocument, RectorDispositionDocument, \
    NecessityRequestDocument, DocumentType
from TextMissing.utils.version_handler import VersionHandler
from TextMissing.utils.xlsbuilder import XlsBuilder
from text_missing import settings


class  DocumentManager:
    def __init__(self):
        pass
    @staticmethod
    def __add_uploaded_document(document_name, author,abstract,keywords,status,file):
        instance = UploadedDocument()
        instance.document_name = document_name
        instance.author = author
        instance.abstract = abstract
        instance.keywords = keywords
        instance.status = status
        instance.file = file
        instance.save()
        instance.size = instance.file.size
        instance.save()

    @staticmethod
    def __add_rector_disposition_document(document_name, author,abstract,keywords,status, user):
        instance = RectorDispositionDocument()
        instance.document_name = document_name
        instance.author = author
        instance.abstract = abstract
        instance.keywords = keywords
        instance.status = status
        set_file_content(instance, instance.document_name + ".docx", DocumentManager.make_doc(user))

        instance.save()
        instance.size = instance.file.size
        instance.save()

    @staticmethod
    def __add_necessity_request_document(document_name, author,abstract,keywords,status,user):

        instance = NecessityRequestDocument()
        instance.document_name = document_name
        instance.author = author
        instance.abstract = abstract
        instance.keywords = keywords
        instance.status = status
        xl = XlsBuilder()
        xl.set_content(user)
        xl.save()
        set_file_content(instance, instance.document_name + ".xlsx", xl.file_name)
        instance.save()
        instance.size = instance.file.size
        instance.save()

    @staticmethod
    def __update_uploaded_document(idx,document_name,abstract,keywords,status,file):
        instance = UploadedDocument.objects.filter(id=idx).first()
        instance.document_name = document_name
        instance.abstract = abstract
        instance.keywords = keywords
        instance.status = status
        new_file = file
        if new_file and new_file != instance.file:
            instance.file = new_file
        instance.version = VersionHandler.upgradeVersion(instance)
        instance.save()
        instance.size = instance.file.size
        instance.save()

    @staticmethod
    def __update_rector_disposition_document(idx,document_name,abstract,keywords,status, user):
            instance = RectorDispositionDocument.objects.filter(id=idx).first()
            instance.document_name = document_name
            instance.abstract = abstract
            instance.keywords = keywords
            instance.status = status
            set_file_content(instance, instance.document_name + ".docx", DocumentManager.make_doc(user))
            instance.save()
            instance.size = instance.file.size
            instance.version = VersionHandler.upgradeVersion(instance)
            instance.save()

    @staticmethod
    def __update_necessity_request_document(idx,document_name,abstract,keywords,status,user):
        instance = NecessityRequestDocument.objects.filter(id=idx).first()
        instance.document_name = document_name
        instance.abstract = abstract
        instance.keywords = keywords
        instance.status = status
        xl = XlsBuilder()
        xl.set_content(user)
        xl.save()
        set_file_content(instance, instance.document_name + ".xlsx", xl.file_name)
        instance.save()
        instance.size = instance.file.size
        instance.version = VersionHandler.upgradeVersion(instance)
        instance.save()

    @staticmethod
    def add_document(type, document_name, author, abstract, keywords, status,param = None):
            switcher = {
                DocumentType.UPLOADED: DocumentManager.__add_uploaded_document,
                DocumentType.DR: DocumentManager.__add_rector_disposition_document,
                DocumentType.RN: DocumentManager.__add_necessity_request_document
            }
            switcher[type](document_name,author,abstract,keywords,status,param)

    @staticmethod
    def update_document(idx,type,document_name,abstract,keywords,status, param):
        switcher = {
            DocumentType.UPLOADED: DocumentManager.__update_uploaded_document,
            DocumentType.DR: DocumentManager.__update_rector_disposition_document,
            DocumentType.RN: DocumentManager.__update_necessity_request_document
        }
        switcher[type](idx,document_name,abstract,keywords,status,param)

    @staticmethod
    def remove_document(self,idx):
        files = Document.objects.filter(id=idx)
        os.remove(os.path.join(settings.MEDIA_ROOT, files.first().file.name))
        files.delete()

    @staticmethod
    def make_doc(user):
        doc = DocxTemplate("templates/doc-templates/dr.docx")
        context = {'user_name': user}
        doc.render(context)
        filePath = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        doc.save(filePath)
        return filePath

def set_file_content(instance, name, path):
    with open(path, 'rb') as f:
        instance.file.save(name, f, save=False)
    os.remove(path)