from django.conf.urls import patterns, url

from app1 import views

urlpatterns = [
    # /app1
    url(r'^$', views.IndexView.as_view(), name='index'),
    # /polls/5/
    url(r'^test/$', views.test, name='test'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),

    # ex: /polls/5/results/
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<name_id>\d+)/priority/$', views.priority, name='priority'),
]
