from django.db import models


# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return ' '.join([
            self.first_name,
            self.last_name,])
    
class Phone(models.Model):
    

    phone_number = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Person)
    
    def __str__(self):
        return ' '.join([
            self.phone_number,
            str(self.owner)])