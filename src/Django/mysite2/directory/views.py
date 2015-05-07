from django.views.generic import ListView
from django.core.urlresolvers import reverse
from django.views.generic import CreateView

from directory.models import Person
from directory.models import Phone

import directory.forms as forms 

## Listing

class ListPersonView(ListView):

    model = Person
    template_name = 'person_list.html'
    
class ListPhoneView(ListView):

    model = Phone
    template_name = 'phone_list.html'


## Creating
class CreatePersonView(CreateView):
    
    # To avoid the exception:
    #Using ModelFormMixin (base class of CreatePersonView) without the 'fields' attribute is prohibited.
    fields = "__all__" 
    
    model = Person
    template_name = 'edit_person.html'

    def get_success_url(self):
        return reverse('person-list')


class CreatePhoneView(CreateView):
    
    # If a custom form is added we have to delete the fields!
    #fields = "__all__" 
    form_class = forms.PhoneForm
    
    model = Phone
    template_name = 'edit_phone.html'
    

    def get_success_url(self):
        return reverse('phone-list')


