from django.conf.urls import url
from django.views.static import serve

from text_missing import settings
from . import views

app_name = "TextMissing"
urlpatterns = [
    url(r'^documents/$', views.documents_page, name='documents'),
    url(r'^documents/delete/(?P<document_id>.*)', views.delete_document, name='delete_document'),
    url(r'^upload_document/$', views.upload_document, name='upload'),
    url(r'^zones/$',views.zones,name='zones'),
    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
