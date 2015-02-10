from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from forms import NameForm


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('app2/name.html')
            return render(request, 'app2/name.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'app2/name.html', {'form': form})