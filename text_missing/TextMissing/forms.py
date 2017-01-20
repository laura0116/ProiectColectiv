import datetime
import os
import random
import string

from django.core.files import File
from django.forms import Form, CharField, IntegerField, DateField, FileField, ModelForm
from docxtpl import DocxTemplate
import jinja2

from TextMissing.models import StatusChoices, Document
from TextMissing.utils.xlsbuilder import XlsBuilder


class UploadDocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('document_name', 'abstract', 'keywords', 'file')

    def __init__(self, user, *args, **kwargs):
        super(UploadDocumentForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = Document()
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


class RectorDispositionForm(ModelForm):
    class Meta:
        model = Document
        fields = ('document_name', 'abstract', 'keywords')

    def __init__(self, user, *args, **kwargs):
        super(RectorDispositionForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = Document()
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
        model = Document
        fields = ('document_name', 'abstract', 'keywords')

    def __init__(self, user, *args, **kwargs):
        super(NecessityRequestForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = Document()
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