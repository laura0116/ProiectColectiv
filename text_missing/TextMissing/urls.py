from django.conf.urls import url

from . import views

app_name = "TextMissing"
urlpatterns = [
    url(r'^documents/$', views.documents_page, name='documents'),
    url(r'^documents/delete/(?P<document_id>.*)', views.delete_document, name='delete_document'),
]
