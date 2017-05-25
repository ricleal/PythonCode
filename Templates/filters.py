from django import template

# --- Filters
register = template.Library()  # pylint: disable=C0103


@register.filter(name='star_wrap')
def star_wrap(value):
    return "** " + value + " **"


@register.simple_tag(takes_context=True)
def fullpath(context, arg):
    print(context)
    return "/tmp/"+str(arg)
