from django.conf.urls import patterns, url

import directory.views


urlpatterns = patterns('',
    url(r'^person/$', directory.views.ListPersonView.as_view(), name='person-list',),
    url(r'^phone/$', directory.views.ListPhoneView.as_view(), name='phone-list',),
    
    url(r'^person/new$', directory.views.CreatePersonView.as_view(), name='person-new',),
    url(r'^phone/new$', directory.views.CreatePhoneView.as_view(), name='phone-new',),
)