import datetime
import os

from django.forms import Form, CharField, IntegerField, DateField, FileField, ModelForm

from TextMissing.models import StatusChoices, Document
from text_missing import settings


class AddDocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('document_name', 'abstract', 'keywords', 'file')

    def __init__(self, user, *args, **kwargs):
        super(AddDocumentForm, self).__init__(*args, **kwargs)
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
            os.remove(os.path.join(settings.MEDIA_ROOT, instance.file.name))
            instance.file = new_file
            instance.size = instance.file.size / 1048576.0
        if commit:
            instance.save()
        return instance
