from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from app1.models import Name
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'app1/index.html'
    context_object_name = 'latest_name_list'

    def get_queryset(self):
        """Return the last five published Names."""
        return Name.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Name
    template_name = 'app1/detail.html'
    

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

class ResultsView(generic.DetailView):
    model = Name
    template_name = 'app1/results.html'