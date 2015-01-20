from django.conf.urls import patterns, url

from app1 import views

urlpatterns = patterns('',
    # /app1
    url(r'^$', views.index, name='index'),
    # /polls/5/
    url(r'^(?P<name_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<name_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<name_id>\d+)/vote/$', views.vote, name='vote'),
)
