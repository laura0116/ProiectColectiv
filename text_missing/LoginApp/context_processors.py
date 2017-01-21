from django.conf.urls import url
from django.core.urlresolvers import reverse, resolve


def basics_processors(request):
    return {'site_title': "TextMissing Document Management App", 'main_url': reverse("LoginApp:main")}
