from book.models import Book
from django.views import generic


class ListView(generic.ListView):
    model = Book