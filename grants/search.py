from django.template import RequestContext
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.http import HttpResponse
from django.utils import simplejson
import json
import csv
import logging
from models import *
from django.template.defaultfilters import slugify
from django.db.models.loading import get_model

NO_EXIST_OBJECT = {
  "error": "Resource not found",
  "message": "Couldn't find Object"
}

def search(request):
    return render_to_response('grants/grant_application/search.html', context_instance=RequestContext(request))

def results(request):
    grant_applications = search_grant_applications(request.REQUEST)
    template = loader.get_template('grants/grant_application/results.html')
    context  = Context({'grant_applications': grant_applications, })
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
def api_grant_applications(request):
    try:
        grant_applications = search_grant_applications(request.REQUEST)
    except GrantApplication.DoesNotExist:
        return HttpResponse(json.dumps(NO_EXIST_OBJECT))
    return HttpResponse(serializers.serialize('json', grant_applications))

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

# These Endpoints return csv
def csv_show_grant_application(request, grant_application_id):
    try:
        grant_application = GrantApplication.objects.filter(id=grant_application_id)
    except GrantApplication.DoesNotExist:
        return HttpResponse(json.dumps(NO_EXIST_OBJECT))
    return export(grant_application)

def csv_grant_applications(request):
    try:
        grant_application = search_grant_applications(request.REQUEST)
    except GrantApplication.DoesNotExist:
        return HttpResponse(json.dumps(NO_EXIST_OBJECT))
    return export(grant_application)


# Export as csv
def export(qs, fields=None):
    model = qs.model
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % slugify(model.__name__)
    writer = csv.writer(response)
    # Write headers to CSV file
    if fields:
        headers = fields
    else:
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
    writer.writerow(headers)
    # Write data to CSV file
    for obj in qs:
        row = []
        for field in headers:
            if field in headers:
                val = getattr(obj, field)
                if callable(val):
                    val = val()
                row.append(val)
        writer.writerow(row)
    # Return CSV file to browser as download
    return response


# MISC
def search_grant_applications(options):
    logging.info(options)
    # TODO: DON'T LET THIS PULL DOWN THE WHOLE DB
    results = GrantApplication.objects.filter()
    if 'grantee' in options:
        results = results.filter(organization__name__contains=options['grantee'])

    # TODO: The other params should actually affect the search results!!
    # results = results.filter(organization__city__contains=options['city'])
    # results = results.filter(organization__state__contains=options['state'])
    # Similar thing for giving project type(WHAT KEY IS THIS!?!?)
    # results = results.filter(grant_cycle__title__contains='')
    # results = results.filter(submission_time__year=options['year'])

    results2 = []
    for r in results[:]:
        pts = r.grant_cycle.givingproject_set.all()
        for pt in pts[:]:
            if pt.title == options['project_type']:
                results2.append(r)

    return results2
