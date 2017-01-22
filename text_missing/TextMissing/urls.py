from django.conf.urls import url
from django.views.static import serve

from text_missing import settings
from . import views

app_name = "TextMissing"
urlpatterns = [
    url(r'^documents/$', views.documents_page, name='documents'),
    url(r'^documents/delete_document/(?P<document_id>.*)', views.delete_document, name='delete_document'),
    url(r'^documents/update/(?P<document_id>.*)', views.update_document, name='update_document'),
    url(r'^documents/view_versions/(?P<document_id>.*)', views.view_versions, name='view_versions'),
    url(r'^add_document/(?P<document_type>.*)$', views.add_document, name='upload'),
    url(r'^zones/$', views.zones, name='zones'),
    url(r'^zones/work_zone/$', views.work_zone, name='work_zone'),
    url(r'^zones/initiated_zone/$', views.initiate_zone, name='initiated_zone'),
    url(r'^zones/task_zone/$', views.task_zone, name='task_zone'),
    url(r'^zones/finished_zone/$', views.finished_zone, name='finished_zone'),
    url(r'^flows/$',views.flows_page,name="flows"),
    url(r'^add_flow/$', views.add_flow_page, name="add_flow"),
    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
