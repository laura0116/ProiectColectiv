import math
from django.db import models

# Create your models here.
from LoginApp.models import Client


class StatusChoices:
    DRAFT = "draft"
    FINAL = "final"
    FINAL_REVISED = "finalRevised"
    BLOCKED = "blocked"
    CHOICES = (
        (DRAFT, "Draft"),
        (FINAL, "Final"),
        (FINAL_REVISED, "Final revised"),
        (BLOCKED, "Blocked")
    )


class DocumentType:
    UPLOADED = 'uploaded'
    DR = 'rector disposition'
    RN = 'necessity request'
    CHOICES = (
        (UPLOADED, "Uploaded"),
        (DR, "Rector disposition"),
        (RN, "Necessity request")
    )


class FlowType:
    RECTOR_DISPOSITION = 'rector disposition'
    NECESSITY_REQUEST = 'necessity request'
    CHOICES = (
        (RECTOR_DISPOSITION, 'Rector Disposition'),
        (NECESSITY_REQUEST, "Necessity Request"),
    )


class DocumentFlow(models.Model):
    name = models.CharField(max_length=30)
    flow_type = models.CharField(max_length=30, choices=FlowType.CHOICES)
    initiator = models.ForeignKey(Client, null=False, default=0)
    creation_date = models.DateField(auto_now_add=True)
    state = models.PositiveIntegerField(default=0)

    def execute_flow(self, flow_function, *params):
            flow_function(self, *params)

    def documents_in_flow(self):
        return "\n".join([document.document_name + ", " for document in self.documents.all()])

    def __str__(self):
        return self.name + " by " + str(self.initiator)


class Document(models.Model):
    document_name = models.CharField(max_length=64)
    author = models.ForeignKey(Client, null=False, default=1)
    size = models.FloatField(default=0)
    version = models.CharField(max_length=64, default=0.1)
    creation_date = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)
    abstract = models.CharField(max_length=100)
    keywords = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=StatusChoices.CHOICES)
    file = models.FileField(upload_to='documents/%Y%m%d', null=True, blank=True)
    type = models.CharField(max_length=20, choices=DocumentType.CHOICES, default=DocumentType.UPLOADED)
    flow = models.ForeignKey(DocumentFlow, related_name="documents", null=True, default=None)

    def get_file_url(self):
        if self.file:
            return '/media/' + str(self.file)

    def get_file_name(self):
        return str(self.file).split("/")[-1]


class UploadedDocument(Document):
    def save(self, *args, **kwargs):
        self.type = DocumentType.UPLOADED
        super(Document, self).save(*args, **kwargs)


class NecessityRequestDocument(Document):
    def save(self, *args, **kwargs):
        self.type = DocumentType.RN
        super(Document, self).save(*args, **kwargs)


class RectorDispositionDocument(Document):
    def save(self, *args, **kwargs):
        self.type = DocumentType.DR
        super(Document, self).save(*args, **kwargs)



