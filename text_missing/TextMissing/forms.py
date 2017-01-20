import datetime
import os
import random
import string

from django.core.files import File
from django.forms import Form, CharField, IntegerField, DateField, FileField, ModelForm, forms
from docxtpl import DocxTemplate
import jinja2

from TextMissing.models import StatusChoices, Document, UploadedDocument, RectorDispositionDocument, \
    NecessityRequestDocument
from TextMissing.utils.xlsbuilder import XlsBuilder

class AddDocumentForm(ModelForm):
    class Meta:
        model = UploadedDocument
        fields = ('document_name', 'abstract', 'keywords', 'file')

    def __init__(self, user, *args, **kwargs):
        super(AddDocumentForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_file(self):
        if self.cleaned_data['file'] is None:
            raise forms.ValidationError("A file must be chosen for upload")


    def save(self, commit=True):
        instance = UploadedDocument()
        instance.document_name = self.cleaned_data['document_name']
        instance.author = self.user
        instance.version = 0
        instance.abstract = self.cleaned_data['abstract']
        instance.keywords = self.cleaned_data['keywords']
        instance.status = StatusChoices.DRAFT
        instance.file = self.cleaned_data['file']
        instance.size = instance.file.size / 1048576.0
        if commit:
            instance.save(self)
        return instance


class UpdateDocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('document_name', 'abstract', 'keywords', 'file')

    def __init__(self, user, document_id, *args, **kwargs):
        super(UpdateDocumentForm, self).__init__(*args, **kwargs)
        self.user = user
        self.document_id = document_id

    def save(self, commit=True):
        instance = Document.objects.filter(id=self.document_id).first()
        instance.document_name = self.cleaned_data['document_name']
        instance.abstract = self.cleaned_data['abstract']
        instance.keywords = self.cleaned_data['keywords']
        new_file = self.cleaned_data['file']
        if new_file != instance.file:
            instance.file = new_file
            instance.size = instance.file.size / 1048576.0
        if commit:
            instance.save()
        return instance


class RectorDispositionForm(ModelForm):
    class Meta:
        model = RectorDispositionDocument
        fields = ('document_name', 'abstract', 'keywords')

    def __init__(self, user, *args, **kwargs):
        super(RectorDispositionForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = RectorDispositionDocument()
        instance.document_name = self.cleaned_data['document_name']
        instance.author = self.user
        instance.version = 0
        instance.abstract = self.cleaned_data['abstract']
        instance.keywords = self.cleaned_data['keywords']
        instance.status = StatusChoices.DRAFT
        set_file_content(instance, instance.document_name + ".docx", self.make_doc())
        instance.size = instance.file.size / 1048576.0
        if commit:
            instance.save(self)
        return instance

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
        instance = NecessityRequestDocument()
        instance.document_name = self.cleaned_data['document_name']
        instance.author = self.user
        instance.version = 0
        instance.abstract = self.cleaned_data['abstract']
        instance.keywords = self.cleaned_data['keywords']
        instance.status = StatusChoices.DRAFT
        xl = XlsBuilder()
        xl.set_content({"UserName": str(self.user)})
        xl.save()
        set_file_content(instance, instance.document_name + ".xlsx", xl.file_name)
        instance.size = instance.file.size / 1048576.0
        if commit:
            instance.save(self)
        return instance


def set_file_content(instance, name, path):
    with open(path, 'rb') as f:
        instance.file.save(name, f, save=False)
    os.remove(path)