from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='book/home.html'), name='home'),
    path('<slug:argument>/', views.generic_list, name='list'),

]