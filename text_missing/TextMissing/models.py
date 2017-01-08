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


class Document(models.Model):
    document_name = models.CharField(max_length=64)
    author = models.ForeignKey(Client, null=False, default=1)
    size = models.IntegerField(default=0)
    version = models.CharField(max_length=64)
    creation_date = models.DateField()
    last_update = models.DateField()
    abstract = models.CharField(max_length=100)
    keywords = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=StatusChoices.CHOICES)
    file = models.FileField(upload_to='documents/%Y%m%d', null=True, blank=True)

    def get_document_url(self):
        if self.file:
            return 'http://localhost:8000/media/' + str(self.file)
