from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.template import RequestContext, loader

from app1.models import Name


def index(request):
    latest_name_list = Name.objects.order_by('-pub_date')[:5]
    context = {'latest_name_list': latest_name_list}
    return render(request, 'app1/index.html', context)


# Create your views here.
def detail(request, name_id):
    try:
        name = Name.objects.get(pk=name_id)
    except Name.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'app1/detail.html', {'name': name})

def results(request, name_id):
    response = "You're looking at the results of name %s."
    return HttpResponse(response % name_id)

def vote(request, name_id):
    return HttpResponse("You're voting on question %s." % name_id)