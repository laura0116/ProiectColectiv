from django.conf.urls import url

from . import views

app_name = "TextMissing"
urlpatterns = [
    url(r'^documents/', views.documents_page, name='documents'),
]
