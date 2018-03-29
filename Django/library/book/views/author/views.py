from book.models import Author
from django.views import generic


class ListView(generic.ListView):
    model = Author