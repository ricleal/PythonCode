from book.models import Publisher
from django.views import generic


class ListView(generic.ListView):
    model = Publisher