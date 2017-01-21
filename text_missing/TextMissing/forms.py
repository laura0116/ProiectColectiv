import datetime
import os
import random
import string

from django.core.files import File
from django.forms import Form, CharField, IntegerField, DateField, FileField, ModelForm, forms
from docxtpl import DocxTemplate
import jinja2

from TextMissing.models import StatusChoices, Document, UploadedDocument, RectorDispositionDocument, \
    NecessityRequestDocument, DocumentType
from TextMissing.utils import document_manager
from TextMissing.utils.document_manager import DocumentManager
from TextMissing.utils.version_handler import VersionHandler
from TextMissing.utils.xlsbuilder import XlsBuilder


class AddDocumentForm(ModelForm):
    class Meta:
        model = UploadedDocument
        fields = ('document_name', 'abstract', 'keywords', 'file')

    def __init__(self, user, *args, **kwargs):
        super(AddDocumentForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        if self.cleaned_data['file'] is None:
            raise forms.ValidationError("A file must be chosen for upload")

    def save(self, commit=True):
        DocumentManager.add_document(DocumentType.UPLOADED,
                                     self.cleaned_data['document_name'],
                                     self.user,
                                     self.cleaned_data['abstract'],
                                     self.cleaned_data['keywords'],
                                     StatusChoices.DRAFT,
                                     self.cleaned_data['file'])



class RectorDispositionForm(ModelForm):
    class Meta:
        model = RectorDispositionDocument
        fields = ('document_name', 'abstract', 'keywords')

    def __init__(self, user, *args, **kwargs):
        super(RectorDispositionForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        DocumentManager.add_document(DocumentType.DR,
                                     self.cleaned_data['document_name'],
                                     self.user, self.cleaned_data['abstract'],
                                     self.cleaned_data['keywords'],
                                     StatusChoices.DRAFT)

    def make_doc(self):
        doc = DocxTemplate("templates/doc-templates/dr.docx")
        context = {'user_name': str(self.user)}
        doc.render(context)
        # TODO: maybe construct a random path for the temporary file
        filePath = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        doc.save(filePath)
        return filePath


class NecessityRequestForm(ModelForm):
    class Meta:
        model = NecessityRequestDocument
        fields = ('document_name', 'abstract', 'keywords')

    def __init__(self, user, *args, **kwargs):
        super(NecessityRequestForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        DocumentManager.add_document(DocumentType.RN,
                                     self.cleaned_data['document_name'],
                                     self.user,
                                     self.cleaned_data['abstract'],
                                     self.cleaned_data['keywords'],
                                     StatusChoices.DRAFT,
                                     {"UserName": str(self.user)})

class UpdateDocumentForm(ModelForm):
    class Meta:
        model = UploadedDocument
        fields = ('document_name', 'abstract', 'keywords', 'status', 'file')

    def __init__(self, user, document_id, *args, **kwargs):
        super(UpdateDocumentForm, self).__init__(*args, **kwargs)
        self.user = user
        self.document_id = document_id

    def save(self, commit=True):
        DocumentManager.update_document(self.document_id,DocumentType.UPLOADED, self.cleaned_data['document_name'], self.cleaned_data['abstract'], self.cleaned_data['keywords'],self.cleaned_data['status'],self.cleaned_data['file'])


class UpdateRectorDisposition(ModelForm):
    class Meta:
        model = RectorDispositionDocument
        fields = ('document_name', 'abstract', 'keywords', 'status')

    def __init__(self, user, document_id, *args, **kwargs):
        super(UpdateRectorDisposition, self).__init__(*args, **kwargs)
        self.user = user
        self.document_id = document_id

    def save(self, commit=True):
        DocumentManager.update_document(self.document_id, DocumentType.DR,
                                        self.cleaned_data['document_name'],
                                        self.cleaned_data['abstract'],
                                        self.cleaned_data['keywords'],
                                        self.cleaned_data['status'],
                                        {'user_name': str(self.user)})


    def make_doc(self):
        doc = DocxTemplate("templates/doc-templates/dr.docx")
        context = {'user_name': str(self.user)}
        doc.render(context)
        # TODO: maybe construct a random path for the temporary file
        filePath = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        doc.save(filePath)
        return filePath


class UpdateNecessityRequest(ModelForm):
    class Meta:
        model = NecessityRequestDocument
        fields = ('document_name', 'abstract', 'keywords', 'status')

    def __init__(self, user, document_id, *args, **kwargs):
        super(UpdateNecessityRequest, self).__init__(*args, **kwargs)
        self.user = user
        self.document_id = document_id

    def save(self, commit=True):
        DocumentManager.update_document(self.document_id, DocumentType.RN,
                                        self.cleaned_data['document_name'],
                                        self.cleaned_data['abstract'],
                                        self.cleaned_data['keywords'],
                                        self.cleaned_data['status'],
                                        {"UserName": str(self.user)})




def set_file_content(instance, name, path):
    with open(path, 'rb') as f:
        instance.file.save(name, f, save=False)
    os.remove(path)