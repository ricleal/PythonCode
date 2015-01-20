from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from app1.models import Name


def index(request):
    latest_name_list = Name.objects.order_by('-pub_date')[:5]
    context = {'latest_name_list': latest_name_list}
    return render(request, 'app1/index.html', context)


# Create your views here.
def detail(request, name_id):
    name = get_object_or_404(Name, pk=name_id)
    return render(request, 'app1/detail.html', {'name': name})

def results(request, name_id):
    response = "You're looking at the results of name %s."
    return HttpResponse(response % name_id)

def priority(request, name_id):
    p = get_object_or_404(Name, pk=name_id)
    try:
        selected_phone = p.phone_set.get(pk=request.POST['phone'])
    except (KeyError, Name.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'app1/detail.html', {
            'name': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_phone.phone_priority += 1
        selected_phone.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('app1:results', args=(p.id,)))