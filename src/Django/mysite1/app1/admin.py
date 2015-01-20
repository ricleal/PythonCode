from django.contrib import admin
from app1.models import Name, Phone

# Register your models here.

class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 3


class NameAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Person name information', {'fields': ['firstname_text', 'lastname_text']}),
        ('Date information', {'fields': ['pub_date'],
        	'classes': ['collapse']}),
    ]
    inlines = [PhoneInline]
    search_fields = ['firstname_text', 'lastname_text']
    list_display = ('firstname_text', 'lastname_text', 'was_published_recently')
    list_filter = ['pub_date']

admin.site.register(Name, NameAdmin)
admin.site.register(Phone)
