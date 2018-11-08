"""chise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from chise.core.views import *
from chise import settings


admin.site.site_header = settings.PROJECT_NAME
admin.site.site_title = settings.PROJECT_NAME
admin.site.index_title = _('Administration')

urlpatterns = i18n_patterns(
    path('', admin.site.urls),
    path('vnc', VNCView.as_view(), name='vnc'),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
            url(r'^rosetta/', include('rosetta.urls'))
    ]
