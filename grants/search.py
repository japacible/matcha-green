from django.template import RequestContext
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.http import HttpResponse
from django.utils import simplejson
import json
from models import *

NO_EXIST_OBJECT = {
  "error": "Resource not found",
  "message": "Couldn't find Object"
}

def search(request):
    return render_to_response('grants/grant_application/search.html', context_instance=RequestContext(request))

def results(request):
    grant_applications = GrantApplication.objects.all()
    template = loader.get_template('grants/grant_application/results.html')
    context  = Context({
        'grant_applications': grant_applications, })
    return HttpResponse(template.render(context))


def show(request, grant_application_id):
    grant_application = GrantApplication.objects.get(id=grant_application_id)
    grantee  = grant_application.organization
    template = loader.get_template('grants/grant_application/show.html')
    context  = Context({
        'grant_application': grant_application,
        'grantee': grantee,
    })
    return HttpResponse(template.render(context))

# These Endpoints return serialized json
def api_show_grant_application(request, grant_application_id):
    try:
        grant_application = GrantApplication.objects.get(id=grant_application_id)
    except GrantApplication.DoesNotExist:
        return HttpResponse(json.dumps(NO_EXIST_OBJECT))
    return HttpResponse(serializers.serialize('json', [grant_application]))

def api_show_grantee(request, grantee_id):
    try:
        grantee = Grantee.objects.get(id=grantee_id)
    except Grantee.DoesNotExist:
        return HttpResponse(json.dumps(NO_EXIST_OBJECT))
    return HttpResponse(serializers.serialize('json', [grantee]))

def api_show_grant_cycle(request, grant_cycle_id):
    try:
        grant_cycle = GrantCycle.objects.get(id=grant_cycle_id)
    except GrantCycle.DoesNotExist:
        return HttpResponse(json.dumps(NO_EXIST_OBJECT))
    return HttpResponse(serializers.serialize('json', [grant_cycle]))
