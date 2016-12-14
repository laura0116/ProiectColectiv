from django.db import models

# Create your models here.
from text_missing.LoginApp.models import Client

class StatusChoices:
    DRAFT = 'Draft'
    FINAL = 'Final'
    FINAL_REVISED = 'Final revised'
    BLOCKED = 'Blocked'
    CHOICES = [(DRAFT,FINAL,FINAL_REVISED,BLOCKED)]

class Document(models.Model):
    documentName = models.CharField(max_length=64)
    author = models.ForeignKey(Client.type("contributor", "admin", "manager"), null=False, default=1)
    size = models.IntegerField(default=0)
    version = models.CharField(max_length=64)
    creation_date = models.DateField()
    last_update = models.DateField()
    abstract = models.CharField(max_length=100)
    keywords = models.CharField(max_length=100)
    status = models.CharField(max_length=20,choices=StatusChoices.CHOICES)




