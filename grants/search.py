from django.template import RequestContext
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponse

def search(request):
    return render_to_response('grants/grant_application/search.html', context_instance=RequestContext(request))

def results(request):
    return render_to_response('grants/grant_application/results.html', context_instance=RequestContext(request))

def show(request, grant_application_id):
    return render_to_response('grants/grant_application/show.html', {'grant':
           grant_application_id}, context_instance=RequestContext(request))
