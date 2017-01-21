import os

from TextMissing.forms import *
from TextMissing.models import StatusChoices, Document, UploadedDocument, RectorDispositionDocument, \
    NecessityRequestDocument, DocumentType, DocumentVersion
from TextMissing.utils.version_handler import VersionHandler
from TextMissing.utils.xlsbuilder import XlsBuilder
from text_missing import settings


class  DocumentManager:
    def __init__(self):
        pass
    @staticmethod
    def __add_uploaded_document(document_name, author,abstract,keywords,status,file):
        instance = DocumentVersion()
        instance.document_name = document_name
        instance.author = author
        instance.abstract = abstract
        instance.keywords = keywords
        instance.file = file
        instance.save()
        instance.size = instance.file.size / (1024.0 * 1024)
        instance.save()

        doc = UploadedDocument()
        doc.status = status
        doc.save()
        doc.versions.add(instance)
        doc.save()

    @staticmethod
    def __add_necessity_request_document(document_name, author,abstract,keywords,status,user):
        instance = DocumentVersion()
        instance.document_name = document_name
        instance.author = author
        instance.abstract = abstract
        instance.keywords = keywords
        xl = XlsBuilder()
        xl.set_content(user)
        xl.save()
        set_file_content(instance, instance.document_name + ".xlsx", xl.file_name)
        instance.save()
        instance.size = instance.file.size / (1024.0 * 1024)
        instance.save()

        doc = NecessityRequestDocument()
        doc.status = status
        doc.save()
        doc.versions.add(instance)
        doc.save()

    @staticmethod
    def __update_uploaded_document(idx,document_name,abstract,keywords,status,file):
        docInstance = UploadedDocument.objects.filter(id=idx).first()
        docInstance.status = status

        instance = DocumentVersion()
        instance.document_name = document_name
        instance.abstract = abstract
        instance.keywords = keywords
        if file:
            instance.file = file
        else:
            instance.file = docInstance.file
        instance.author = docInstance.author
        instance.version = VersionHandler.upgradeVersion(docInstance)
        instance.save()
        instance.size = instance.file.size / (1024.0 * 1024)
        instance.save()
        docInstance.save()
        docInstance.versions.add(instance)
        docInstance.save()

    @staticmethod
    def __create_instance_dr(instance, document_name,abstract,keywords,status,context):
        ver_instance = DocumentVersion()
        ver_instance.document_name = document_name
        ver_instance.abstract = abstract
        ver_instance.keywords = keywords
        ver_instance.author = instance.author
        ver_instance.save()
        instance.status = status
        instance.city = context['city']
        instance.sum = context['cost']
        instance.phone_number = context['phone_number']
        instance.country = context['actual_country']
        instance.travel_mean = context['travel_mean']
        instance.travel_purpose = context['travel_purpose']
        instance.sum_motivation = context['sum_motivation']
        instance.financing_source = context['financing_source']
        instance.save()
        set_file_content(ver_instance, ver_instance.document_name + ".docx", DocumentManager.make_doc(context))

        ver_instance.save()
        ver_instance.size = ver_instance.file.size / (1024.0 * 1024)
        if len(instance.versions.all()) != 0:
            ver_instance.version = VersionHandler.upgradeVersion(instance)
        ver_instance.save()
        instance.versions.add(ver_instance)
        instance.save()

    @staticmethod
    def __add_rector_disposition_document(document_name, author,abstract,keywords,status, context):
        instance = RectorDispositionDocument()
        instance.author = author
        DocumentManager.__create_instance_dr(instance, document_name,abstract,keywords,status,context)
        instance.save()

    @staticmethod
    def __update_rector_disposition_document(idx,document_name,abstract,keywords,status, context):
        instance = RectorDispositionDocument.objects.filter(id=idx).first()
        DocumentManager.__create_instance_dr(instance, document_name, abstract, keywords, status, context)
        instance.save()

    @staticmethod
    def __update_necessity_request_document(idx,document_name,abstract,keywords,status,user):
        doc_instance = NecessityRequestDocument.objects.filter(id=idx).first()
        doc_instance.status = status
        instance = DocumentVersion()
        instance.document_name = document_name
        instance.abstract = abstract
        instance.keywords = keywords
        xl = XlsBuilder()
        xl.set_content(user)
        xl.save()
        set_file_content(instance, instance.document_name + ".xlsx", xl.file_name)
        instance.save()
        instance.size = instance.file.size / (1024.0 * 1024)
        instance.version = VersionHandler.upgradeVersion(doc_instance)
        instance.save()
        doc_instance.save()
        doc_instance.versions.add(instance)
        doc_instance.save()

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
    def remove_document(idx):
        file = Document.objects.filter(id=idx).first()
        for ver in file.versions.all():
            filepath = os.path.join(settings.MEDIA_ROOT, ver.file.name)
            if os.path.isfile(filepath):
                os.remove(filepath)
        file.versions.all().delete()
        file.delete()

    @staticmethod
    def make_doc(context):
        doc = DocxTemplate("templates/doc-templates/dr.docx")
        doc.render(context)
        filePath = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        doc.save(filePath)
        return filePath


def set_file_content(instance, name, path):
    with open(path, 'rb') as f:
        instance.file.save(name, f, save=False)
    os.remove(path)