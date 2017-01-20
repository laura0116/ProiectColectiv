import datetime
import os

from django.core.files import File
from django.forms import Form, CharField, IntegerField, DateField, FileField, ModelForm
from docxtpl import DocxTemplate
import jinja2

from TextMissing.models import StatusChoices, Document


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
        filePath = self.make_doc()
        with open(filePath, 'rb') as f:
            instance.file.save(instance.document_name + ".docx", f, save=False)
        os.remove(filePath)
        instance.size = instance.file.size / 1048576.0
        if commit:
            instance.save(self)
        return instance

    def make_doc(self):
        doc = DocxTemplate("templates/doc-templates/dr.docx")
        context = {'user_name': str(self.user)}
        doc.render(context)
        filePath = "media/documents/dr_generated.docx"
        doc.save(filePath)
        return filePath
