from django.conf.urls import patterns, url

from app2 import views

urlpatterns = [
    # /app1
    url(r'^name/$', views.get_name, name='name'),

]
