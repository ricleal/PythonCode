from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/app1/')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^app1/', include('app1.urls', namespace="app1")),
    url(r'^app2/', include('app2.urls', namespace="app2")),

)
