from django.template import Template, RequestContext, Engine


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
    context_processors=[
        'context_processors.my_context_processor'
    ],
)

template = Template(
    template_content,
    engine=engine,
)
context = RequestContext(data)

result = template.render(context)

print(result)