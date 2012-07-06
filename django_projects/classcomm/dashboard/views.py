from django.template import RequestContext, loader
from django.http import HttpResponse


def index(request):
    """ Root classcomm project dashboard. """
    
    # Specify template, generate context, and return response
    template = loader.get_template('index.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
# End Def
