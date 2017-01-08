from django.forms import Form, CharField, IntegerField, DateField, FileField, ModelForm

from TextMissing.models import StatusChoices, Document


class UploadDocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ('document_name', 'author', 'size', 'version', 'creation_date', 'last_update', 'abstract', 'keywords', 'status', 'file',)

    def __init__(self, *args, **kwargs):
        super(UploadDocumentForm, self).__init__(*args, **kwargs)

    # def save(self, commit=True):
    #     instance = Document()
    #     instance.document_name = self.cleaned_data['document_name']
    #     instance.author = self.cleaned_data['author']
    #     instance.size = self.cleaned_data['size']
    #     instance.version = self.cleaned_data['version']
    #     instance.creation_date = self.cleaned_data['creation_date']
    #     instance.last_update = self.cleaned_data['last_update']
    #     instance.abstract = self.cleaned_data['abstract']
    #     instance.keywords = self.cleaned_data['keywords']
    #     instance.status = self.cleaned_data['status']
    #
    #     instance2 = DocumentData()
    #     instance2.file = self.cleaned_data['file']
    #     if commit:
    #         instance.save(self)
    #     return instance