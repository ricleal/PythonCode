from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from directory.models import Phone


class PhoneForm(forms.ModelForm):

    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                                    help_text = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
                                    error_message=("ERROR!! Have you written the phone number in right format?.") )
    class Meta:
        model = Phone
        fields = '__all__'
