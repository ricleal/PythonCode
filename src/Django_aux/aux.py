"""
cd /home/rhf/git/reduction_service/src
python manage.py shell
"""

from reduction_service import urls
from django.core.urlresolvers import get_resolver
import pprint as pp

def show_urls(urllist, depth=0):
    for entry in urllist:
        print "  " * depth, entry.regex.pattern
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)




def show_urls2(urllist): 
    resolver = get_resolver(urls)
    for view, regexes in resolver.reverse_dict.iteritems():
        print "\n%s:\n%s" % (view, pp.pformat(regexes))
    
# resolver = get_resolver(urls)
# e = resolver.namespace_dict['eqsans']

def showAllURLs():
    from django.core.urlresolvers import get_resolver
    print get_resolver(None).reverse_dict.keys()

show_urls(urls.urlpatterns)
show_urls2(urls) 