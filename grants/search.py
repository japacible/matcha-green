from django.template import RequestContext
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.http import HttpResponse
import json
from models import *

NO_EXIST_OBJECT = {
  "error": "Resource not found",
  "message": "Couldn't find Object"
}

def search(request):
    return render_to_response('grants/grant_application/search.html', context_instance=RequestContext(request))

def results(request):
    return render_to_response('grants/grant_application/results.html', context_instance=RequestContext(request))

def show(request, grant_application_id):
    return render_to_response('grants/grant_application/show.html', {'grant':
           grant_application_id}, context_instance=RequestContext(request))

def api_show(request, grant_application_id):
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
