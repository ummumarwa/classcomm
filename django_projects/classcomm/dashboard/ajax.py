from django.http import HttpResponse
from datetime import datetime
from django.utils.dateformat import DateFormat


def server_time(request):
    """ AJAX call to get the current server time. """
    
    if request.is_ajax():
        df = DateFormat(datetime.now())
        payload = df.format("F jS Y @ h:iA")
    else:
        payload = "Sorry, this URL is for AJAX calls only."
    return HttpResponse(payload, mimetype="text/plain")
# End Def
