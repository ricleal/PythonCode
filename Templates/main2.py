from django.template import Template, Context, Engine


# --- Main Code

template_content = """ -- HEADER ---
{{ var|star_wrap }}
{% fullpath "filename_123.txt" %}
{{ abc }}
 -- FOOTER ---"""

data = {'var': 'Ricardo'}

engine = Engine(
    debug=True,
    builtins=[
        'filters'
    ],
)

template = Template(
    template_content,
    engine=engine,
)

data.update({'abc': 'def'})
context = Context(data)

result = template.render(context)

print(result)