import datetime
from django.forms import Form, CharField, IntegerField, DateField, FileField, ModelForm

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
