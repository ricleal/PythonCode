from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
import datetime

# Create your models here.

class Name(models.Model):
    firstname_text = models.CharField(max_length=200)
    lastname_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
    	return str(self.firstname_text) + " " + str(self.lastname_text)


    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Phone(models.Model):
    name = models.ForeignKey(Name)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
    	message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=20, validators=[phone_regex], blank=True) # validators should be a list
    def __unicode__(self):
    	return str(self.phone_number)