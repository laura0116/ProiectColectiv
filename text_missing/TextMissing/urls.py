from django.conf.urls import url
from django.views.static import serve

from text_missing import settings
from . import views

app_name = "TextMissing"
urlpatterns = [
    url(r'^documents/$', views.documents_page, name='documents'),
    url(r'^documents/delete_document/(?P<document_id>.*)', views.delete_document, name='delete_document'),
    url(r'^documents/update/(?P<document_id>.*)', views.update_document, name='update_document'),
    url(r'^add_document/$', views.add_document, name='upload'),
    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
