from django import http, template, forms
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.forms.formsets import formset_factory
from django.utils import timezone
import models, datetime, random, logging
import json as simplejson
import grants.models
from fund.decorators import approved_membership
from fund.forms import *

#LOGIN & REGISTRATION
def FundLogin(request):
  printout=''
  if request.method=='POST':
    form = LoginForm(request.POST)
    username = request.POST['email'].lower()
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(Home)
        else:
            printout='Your account is not active.  Contact an administrator.'
            logging.warning("Inactive account tried to log in. Username: "+username)
    else:
        printout ="Your login and password didn't match."
  else:
    form = LoginForm()
  return render_to_response('fund/login.html', {'form':form, 'printout':printout})

def Register(request):
  printout = ''
  if request.method=='POST':
    register = RegistrationForm(request.POST)
    if register.is_valid():
      username = request.POST['email'].lower()
      password = request.POST['password']
      if User.objects.filter(username=username):
        printout = 'That email is already registered.  <a href="/fund/login/">Login</a> instead.'
        logging.info('Email already registered: ' + username)
      else:
        created = User.objects.create_user(username, username, password)
        created.save()
        
        fn = request.POST['first_name']
        ln = request.POST['last_name']
        gp = request.POST['giving_project']
        member = models.Member(first_name=fn, last_name=ln, email=username)
        member.save()
        logging.info('Registration - user and member objects created for '+username)
        if gp:
          giv = models.GivingProject.objects.get(pk=gp)
          membership = models.Membership(member = member, giving_project = giv)
          membership.save()
          member.current = membership.pk
          member.save()      
          logging.info('Registration - membership in ' + giv + ' created')
        user = authenticate(username=username, password=password)
        if user:
          if user.is_active:
            login(request, user)
            return redirect('/fund/registered')
          else: #not active
            printout = 'There was a problem with your registration.  Please contact a site admin for assistance.'
            logging.error('Inactive right after registering. Email: ' + username)
        else: #email & pw didn't match
          printout = 'There was a problem with your registration.  Please contact a site admin for assistance.'
          logging.error("Password didn't match right after registering. Email: " + username)
  else:
    register = RegistrationForm()
    
  return render_to_response('fund/register.html', {'form':register, 'printout':printout})

@login_required(login_url='/fund/login/')
def Registered(request):
  if request.membership_status==0:
    return redirect(NotMember)
  elif request.membership_status==1:
    return redirect(Projects)
  else:
    member = models.Member.objects.get(email=request.user.username)

  nship = request.GET.get('sh') or member.current #sh set by Projects, current set by Register
  try:
    ship = models.Membership.objects.get(pk=nship, member=member)
  except models.Membership.DoesNotExist: #only if they manually entered # or something went horribly wrong
    logging.warning('Membership does not exist right at /registered ' + request.user.username)
    return redirect(Home)
  if ship.approved==True: #another precaution
    logging.warning('Membership approved before check at /registered ' + request.user.username)
    return redirect(Home)
  
  proj = ship.giving_project
  if proj.pre_approved:
    app_list = [email.strip() for email in proj.pre_approved.split(',')]
    logging.info('Checking pre-approval for ' + request.user.username + ' in ' + str(proj) + ', list: ' + proj.pre_approved)
    if ship.member.email in app_list:
      ship.approved = True
      ship.save()
      member.current = nship
      member.save()
      logging.info('Pre-approval succeeded')
      return redirect(Home)

  return render_to_response('fund/registered.html', {'member':member, 'proj':proj})

#MEMBERSHIP MANAGEMENT
@login_required(login_url='/fund/login/')
def Projects(request):
  logging.info('view')
  if request.membership_status==0:
    return redirect(NotMember)
  else:
    member = models.Member.objects.get(email=request.user.username)
  
  ships = member.membership_set.all()
  
  printout = ''
  if request.method=='POST':
    form = AddProjectForm(request.POST)
    if form.is_valid():
      gp = request.POST['giving_project']
      giv = models.GivingProject.objects.get(pk=gp)
      ship, new = models.Membership.objects.get_or_create(member = member, giving_project=giv)
      if new:
        return redirect('/fund/registered?sh='+str(ship.pk))
      else:
        printout = 'You are already registered with that giving project.'
  else:
    form = AddProjectForm()
  return render_to_response('fund/projects.html', {'member':member, 'form':form, 'printout':printout, 'ships':ships})

@login_required(login_url='/fund/login/')
@approved_membership()
def SetCurrent(request, ship_id):
  member = request.membership.member
  try:
    shippy = models.Membership.objects.get(pk=ship_id, member=member, approved=True)
  except models.Membership.DoesNotExist:
    return redirect(Projects)
  
  member.current=shippy.pk
  member.save()
  
  return redirect(Home)
  
# MAIN VIEWS
@login_required(login_url='/fund/login/')
@approved_membership()
def Home(request):

  membership = request.membership
  member = membership.member
  
  #blocks
  news = models.NewsItem.objects.filter(project=membership.giving_project).order_by('-date')
  steps = models.Step.objects.filter(donor__membership=membership, complete=False).order_by('date')[:3]
  events = models.Event.objects.filter(project=membership.giving_project, date__gt=timezone.now()).order_by('date')[:3]
  
  #base
  header = membership.giving_project.title
  
  #home code
  donors = membership.donor_set.all()
  donor_list = list(donors)
  donor_list.sort(key = lambda donor: donor.get_next_date())
  count = donors.count
  notif = membership.notifications
  ContactFormset = formset_factory(MassDonor, extra=5)
  formset = ContactFormset()
  if notif != '': #only show a notification once
    membership.notifications=''
    membership.save()
  
  return render_to_response('fund/home.html', {
                            'homeactive':'true',
                            'header':header,
                            'donors': donor_list,
                            'count':count,
                            'member':member,
                            'news':news,
                            'events':events,
                            'steps':steps,
                            'membership':membership,
                            'notif':notif,
                            'formset':formset})

@login_required(login_url='/fund/login/')
@approved_membership()
def News(request):

  membership = request.membership
  member = membership.member
  
  #blocks
  news = models.NewsItem.objects.filter(project=membership.giving_project).order_by('-date')
  steps = models.Step.objects.filter(donor__membership=membership, complete=False).order_by('date')[:3]
  events = models.Event.objects.filter(project=membership.giving_project, date__gt=timezone.now()).order_by('date')[:3]
  
  #base
  header = membership.giving_project.title
  
  #info specific
  allevents = models.Event.objects.filter(project=project)
  
  #TODO has to be a better way to do this...
  resources = {project.r1title:project.r1link, project.r2title:project.r2link, project.r3title:project.r3link, project.r4title:project.r4link, project.r5title:project.r5link, project.r6title:project.r6link, project.r7title:project.r7link, project.r8title:project.r8link, project.r9title:project.r9link, project.r10title:project.r10link}
  if len(resources)==1: #just nulls
    resources = None
 
  return render_to_response('fund/news.html', {'newsactive':'true',
                                               'header':header,
                                               'news':news,
                                               'events':events,
                                               'member':member,
                                               'steps':steps,
                                               'membership':membership})

@login_required(login_url='/fund/login/')
@approved_membership()
def ScoringList(request):
  
  membership = request.membership
  member = membership.member
  project = membership.giving_project
  
  #blocks
  news = models.NewsItem.objects.filter(project=project).order_by('-date')
  steps = models.Step.objects.filter(donor__membership=membership, complete=False).order_by('date')[:3]
  events = models.Event.objects.filter(project=project, date__gt=timezone.now()).order_by('date')[:3]
  
  #base
  header = project.title
  
  #additional code here!
  
  return render_to_response('fund/info.html', {'3active':'true', 'header':header,
                                                'news':news, 'events':events,
                                                'member':member, 'steps':steps,
                                                'membership':membership})

#ERROR & HELP PAGES
@login_required(login_url='/fund/login/')
def NotMember(request):
  member = request.user #not really member, just for sharing template code
  contact_url=settings.SUPPORT_FORM_URL
  return render_to_response('fund/not_member.html', {'member':member, 'contact_url':contact_url})

@login_required(login_url='/fund/login/')
def NotApproved(request):
  try:
    member = models.Member.objects.get(email=request.user.username)
  except models.Member.DoesNotExist:
    return redirect(NotMember)
  memberships = member.membership_set.all()
  return render_to_response('fund/not_approved.html', {'member':member, 'memberships':memberships})

def Blocked(request):
  contact_url = settings.SUPPORT_FORM_URL
  return render_to_response('fund/blocked.html', {'contact_url':contact_url})

def Support(request):
  header = "Support"
  if request.user:
    member = request.user #for shared template
  return render_to_response('fund/support.html', {'member':member, 'header':header})

#NOT IN USE
@login_required(login_url='/fund/login/')
def Stats(request): #for now, based on django user's admin status
  header = 'SJF Fundraising Admin'
  member = request.user #for sharing template
  if not member.is_staff:
    return redirect('fund/blocked')
    
  #main page shows current projects
  curr_memb = models.Membership.objects.filter(giving_project__fundraising_deadline__gte=timezone.now())
  curr_donors = models.Donor.objects.filter(membership__giving_project__fundraising_deadline__gte=timezone.now())
  
  overall = {}
  overall['parti'] = curr_memb.count()
  overall['contacts'] = curr_donors.count()
  overall['talked'] = curr_donors.filter(talked=True).count()
  overall['asked'] = curr_donors.filter(asked=True).count()
  overall['pledged'] = 0
  overall['gifted'] = 0
  overall['estimated'] = 0
  
  for donor in curr_donors:
    if donor.pledged:
      overall['pledged'] = overall['pledged'] + donor.pledged
    overall['gifted'] = overall['gifted'] + donor.gifted
    overall['estimated'] = overall['estimated'] + donor.amount*donor.likelihood/100
  
  return render_to_response('fund/stats.html', {'member':member, 'header':header, 'overall':overall})

@login_required(login_url='/fund/login/')
def StatsSingle(request, gp_id):
  if not member.admin:
    return redirect('fund/blocked')
  try:
    proj = models.GivingProject.objects.get(pk=gp_id)
  except:
    return redirect(Admin) #add error msg
  members = proj.member_set.all()
  return render_to_response('fund/admin_single.html', {'proj':proj, 'members':members})
  
#FORMS
#successful AJAX should return HttpResponse("success")
@login_required(login_url='/fund/login/')
@approved_membership()
def AddDonor(request):

  membership = request.membership
  action='/fund/add'
  
  if request.method=='POST':
    form = NewDonor(request.POST)
    if form.is_valid():
      donor = models.Donor(firstname = request.POST['firstname'], lastname= request.POST['lastname'], amount= request.POST['amount'], likelihood= request.POST['likelihood'], phone= request.POST['phone'], email= request.POST['email'], membership=membership)
      donor.save()
      membership.last_activity = timezone.now()
      membership.save()
      if request.POST['step_date'] and request.POST['step_desc']:
        step = models.Step(date = request.POST.get('step_date'), description = request.POST['step_desc'], donor = donor)
        step.save()
      return HttpResponse("success")
  else:
    form = NewDonor()

  return render_to_response('fund/add_contact.html', {'form':form, 'action':action})

@login_required(login_url='/fund/login/')
@approved_membership()
def AddMult(request):
  ContactFormset = formset_factory(MassDonor, extra=5)
  if request.method=='POST': #should really only get accessed by post
    formset = ContactFormset(request.POST)
    if formset.is_valid():
      for form in formset.cleaned_data:
        if form:
          contact = models.Donor(firstname = form['firstname'], lastname= form['lastname'], amount= form['amount'], likelihood= form['likelihood'], membership = request.membership)
          contact.save()
      return HttpResponse("success")        
  else:
    formset = ContactFormset()
  return render_to_response('fund/add_mult.html', {'formset':formset})

@login_required(login_url='/fund/login/')
@approved_membership()
def EditDonor(request, donor_id):
  
  try:
    donor = models.Donor.objects.get(pk=donor_id, membership=request.membership)
  except models.Donor.DoesNotExist:
    return redirect(Home) #ADDERROR
    
  action='/fund/'+str(donor_id)+'/edit'
  ajax = request.is_ajax()
  formid = 'editdonor-'+donor_id
  divid = 'donor-'+donor_id
  
  if request.method == 'POST':
    form = models.DonorForm(request.POST, instance=donor)
    if form.is_valid():
      form.save()
      request.membership.last_activity = timezone.now()
      request.membership.save()
      return HttpResponse("success")
  else:
    form = models.DonorForm(instance=donor)

  return render_to_response('fund/edit.html', { 'form': form, 'action':action, 'ajax':ajax, 'divid':divid, 'formid':formid})

@login_required(login_url='/fund/login/')
@approved_membership()
def DeleteDonor(request, donor_id):
  
  try:
    donor = models.Donor.objects.get(pk=donor_id, membership=request.membership)
  except models.Donor.DoesNotExist:
    return redirect(Home) #ADDERROR
    
  action = '/fund/'+str(donor_id)+'/delete'
  
  if request.method=='POST':
    request.membership.last_activity = timezone.now()
    request.membership.save()
    donor.delete()
    return redirect(Home)
    
  return render_to_response('fund/delete.html', {'action':action})

@login_required(login_url='/fund/login/')
@approved_membership()
def AddStep(request, donor_id):
  
  logging.info('Single step - start of view.  User: ' + str(request.membership.member) + ', donor id: ' + str(donor_id))
  
  try:
    donor = models.Donor.objects.get(pk=donor_id, membership=request.membership)
  except models.Donor.DoesNotExist:
    logging.warning('Single step - tried to add step to nonexistent donor.')
    return redirect(Home) #ADDERROR
    
  action='/fund/'+donor_id+'/step'
  ajax = request.is_ajax()
  formid = 'addstep-'+donor_id
  divid = donor_id+'-addstep'
  
  if request.method == 'POST':
    form = models.StepForm(request.POST)
    logging.info('Single step - POST: ' + str(request.POST))
    if form.is_valid() and not donor.get_next_step(): #ADDERROR
      logging.info('Single step - form valid')
      step = form.save(commit = False)
      step.donor = donor
      step.save()
      logging.info('Single step - step saved')
      request.membership.last_activity = timezone.now()
      request.membership.save()
      return HttpResponse("success")
  else: 
    form = models.StepForm()
    
  return render_to_response('fund/add_step.html', {'donor': donor, 'form': form, 'action':action, 'ajax':ajax, 'divid':divid, 'formid':formid})

@login_required(login_url='/fund/login/')
@approved_membership()
def AddMultStep(request):  
  initiald = []
  dlist = []
  size = 0
  for donor in request.membership.donor_set.all():
    if not donor.get_next_step():
      initiald.append({'donor': donor})
      dlist.append(donor)
      size = size +1
  StepFormSet = formset_factory(MassStep, extra=0)
  if request.method=='POST':
    formset = StepFormSet(request.POST)
    logging.info('Multiple steps - posted: ' + str(request.POST))
    if formset.is_valid():
      logging.info('Multiple steps - is_valid passed, cycling through forms')
      for form in formset.cleaned_data:
        if form:
          step = models.Step(donor = form['donor'], date = form['date'], description = form['description'])
          step.save()
          logging.info('Multiple steps - step created')
        else:
          logging.info('Multiple steps - blank form')
      return HttpResponse("success")
  else:
    formset = StepFormSet(initial=initiald)
    logging.info('Multiple steps - loading initial formset, size ' + str(size) + ': ' +str(dlist))
  fd = zip(formset, dlist)
  return render_to_response('fund/add_mult_step.html', {'size':size, 'formset':formset, 'fd':fd, 'multi':True})

@login_required(login_url='/fund/login/')
@approved_membership()
def EditStep(request, donor_id, step_id):
  
  ajax = request.is_ajax()
  
  try:
    donor = models.Donor.objects.get(pk=donor_id, membership=request.membership)
  except models.Donor.DoesNotExist:
    return redirect(Home) #ADDERROR
  
  try:
    step = models.Step.objects.get(id=step_id)
  except models.Step.DoesNotExist:
    return redirect(Home) #ADDERROR
    
  action='/fund/'+str(donor_id)+'/'+str(step_id)+'/'
  formid = 'editstep-'+donor_id
  divid = donor_id+'-nextstep'
  
  if request.method == 'POST':
      form = models.StepForm(request.POST, instance=step)
      if form.is_valid():
        request.membership.last_activity = timezone.now()
        request.membership.save()
        form.save()
        if ajax:
          return HttpResponse("success")
        else:
          return redirect(Home)
  else:
    form = models.StepForm(instance=step)
    
  return render_to_response('fund/edit.html', { 'donor': donor, 'form': form, 'ajax':ajax, 'action':action, 'divid':divid, 'formid':formid})

@login_required(login_url='/fund/login/')
@approved_membership()
def DoneStep(request, donor_id, step_id):
  
  ajax = request.is_ajax()
  membership = request.membership

  try:
    donor = models.Donor.objects.get(pk=donor_id, membership=membership)
  except models.Donor.DoesNotExist:
    return redirect(Home)
  
  try:
    step = models.Step.objects.get(id=step_id, donor=donor)
  except models.Step.DoesNotExist:
    return redirect(Home)
    
  action='/fund/'+str(donor_id)+'/'+str(step_id)+'/done'

  if request.method == 'POST':
    form = StepDoneForm(request.POST)
    if form.is_valid():
      membership.last_activity = timezone.now()
      membership.save()
      step.complete = True
      donor.talked=True
      step.save()
      asked = form.cleaned_data['asked']
      pledged = form.cleaned_data['pledged_amount']
      #share = form.cleaned_data['share']
      news = ' talked to a donor'
      if asked:
        donor.asked=True
        news = ' asked a donor'
      if pledged:
        donor.pledged=pledged
        if pledged>0:
          news = ' got a $'+str(pledged)+' pledge' 
      #if share:
      story = models.NewsItem(short=membership.member.first_name+news, date=timezone.now(), project=membership.giving_project)
      story.save()
      donor.save()
      next = form.cleaned_data['next_step']
      next_date = form.cleaned_data['next_step_date']
      if next!='' and next_date!=None:
        form2 = models.StepForm().save(commit=False)
        form2.date = next_date
        form2.description = next
        form2.donor = donor
        form2.save()
      if ajax:
        return HttpResponse("success")
      else:
        return redirect(Home)
  else:
    form = StepDoneForm()
    
  return render_to_response('fund/done_step.html', {'form':form, 'action':action, 'donor':donor, 'ajax':request.is_ajax()})

#CRON EMAILS
def EmailOverdue(request):
  #TODO - in email content, show all member overdue steps (not just for that ship)
  today = datetime.date.today()
  ships = models.Membership.objects.filter(giving_project__fundraising_deadline__gte=today)
  limit = today-datetime.timedelta(days=7)
  subject, from_email = 'Fundraising Steps', settings.APP_SEND_EMAIL
  for ship in ships:
    user = ship.member
    if ship.has_overdue()>0 and ship.emailed<=limit:
      to = user.email #TODO direct links w/multi gp
      steps = models.Step.objects.filter(donor__membership=ship, date__lt=today, complete=False)
      html_content = render_to_string('fund/email_overdue.html', {'login_url':settings.APP_BASE_URL+'fund/login', 'ship':ship, 'steps':steps, 'base_url':settings.APP_BASE_URL})
      text_content = strip_tags(html_content)
      msg = EmailMultiAlternatives(subject, text_content, from_email, [to], ['sjfnwads@gmail.com'])
      msg.attach_alternative(html_content, "text/html")
      msg.send()
      ship.emailed = today
      ship.save()
  return HttpResponse("")

def NewAccounts(request):
  #Sends GP leaders an email saying how many unapproved memberships there are.  Will continue emailing about the same membership until it's approved/deleted.
  subject, from_email = 'Accounts pending approval', settings.APP_SEND_EMAIL
  for gp in models.GivingProject.objects.all():
    memberships = models.Membership.objects.filter(giving_project=gp, approved=False).count()
    leaders = models.Membership.objects.filter(giving_project=gp, leader=True)
    if memberships>0:
      for leader in leaders:
        to = leader.member.email
        html_content = render_to_string('fund/email_new_accounts.html', {'admin_url':settings.APP_BASE_URL+'admin/fund/membership/', 'count':memberships, 'support_email':settings.APP_SUPPORT_EMAIL})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to], ['sjfnwads@gmail.com'])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
  return HttpResponse("")

def GiftNotify(request):
  #Sends an email to members letting them know gifts have been received
  #Marks donors as notified
  #Puts details in mem notif for main page
  donors = models.Donor.objects.filter(gifted__gt=0, gift_notified=0)
  members = []
  for donor in donors:
    members.append(donor.membership.member)
    donor.membership.notifications += 'Gift of $'+str(donor.gifted)+' received from '+donor.firstname+' '+donor.lastname+'!<br>'
    donor.membership.save()
  unique = set(members)
  subject, from_email = 'Gift received', settings.APP_SEND_EMAIL
  for mem in unique:
    to = mem.email
    html_content = render_to_string('fund/email_gift.html')
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], ['sjfnwads@gmail.com'])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
  donors.update(gift_notified=True)
  return HttpResponse("")

#DEVELOPMENT
def PopulateDB(request):
  if models.GivingProject.objects.count()==0:
  
    #giving projects
    gp = models.GivingProject(title='Olde Giving Project', fund_goal=1000, fundraising_deadline='2008-06-10')
    gp.save()
    gp = models.GivingProject(title='LGBTQ Giving Project', fund_goal=50000, fundraising_deadline='2012-06-17')
    gp.save()
    gp2 = models.GivingProject(title='Environmental Justice Giving Project', fund_goal=50000, fundraising_deadline='2012-07-01')
    gp2.save()
    gp3 = models.GivingProject(title='Next Generation Giving Project', fund_goal=70000, fundraising_deadline='2012-08-25') #NGGP
    gp3.save()
    
    #events (2012 nggp sched)
    event = models.Event(project=gp3, desc='Fundraising Training', date = '2012-06-19 18:00:00')
    event.save()
    event = models.Event(project=gp3, desc='Screening Meeting', date = '2012-08-25 10:00:00')
    event.save()
    event = models.Event(project=gp3, desc='Final Decisions Meeting', date = '2012-09-29 10:00:00')
    event.save()
    event = models.Event(project=gp3, desc='Celebration & Evaluation', date = '2012-10-09 18:00:00')
    event.save()
    event = models.Event(project=gp2, desc='Fundraising Training', date = '2012-06-19 18:00:00')
    event.save()
    event = models.Event(project=gp2, desc='Screening Meeting', date = '2012-08-25 10:00:00')
    event.save()
    event = models.Event(project=gp2, desc='Final Decisions Meeting', date = '2012-09-29 10:00:00')
    event.save()
    event = models.Event(project=gp2, desc='Celebration & Evaluation', date = '2012-10-09 18:00:00')
    event.save()
    
    #users/members - all in ejgp for testing
    
    #sjfnwads account, superuser already, set as leader
    member = models.Member(email='sjfnwads@gmail.com',first_name='Zeke', last_name='Zeke')
    member.save()
    membership = models.Membership(member=member, giving_project=gp2, approved=True, leader=True)
    membership.save()
    
    #aisapatino, scenario#1 - no member object, just user (error!)
    created = User.objects.create_user('aisapatino@gmail.com', 'aisapatino@gmail.com', 'aisa')
    created.save()    
    #member = models.Member(email='aisapatino@gmail.com', first_name='Aisa', last_name='Patino West')
    #member.save()
    #membership = models.Membership(member=member, giving_project=gp2, approved=True)
    #membership.save()
    
    #jessan, scenario#2 - no memberships
    created = User.objects.create_user('jessan@gmail.com', 'jessan@gmail.com', 'jessan')
    created.save()
    member = models.Member(email='jessan@gmail.com',first_name='Jessan', last_name='Hutchison-Quillian')
    member.save()
    #membership = models.Membership(member=member, giving_project=gp2, approved=True)
    #membership.save()
    
    #aisa#2 electrelane, scenario#3 - no approved memberships
    created = User.objects.create_user('electrelane48@gmail.com', 'electrelane48@gmail.com', 'electrelane48')
    created.save()
    member = models.Member(email='electrelane48@gmail.com',first_name='Baisa')
    member.save()
    membership = models.Membership(member=member, giving_project=gp2)
    membership.save()
    
    #donors - 10 per membership
    fname = ['Anna', 'Audrey', 'Jessan', 'Ryan', 'Zeke', 'Kylie', 'Molly', 'Peter', 'Dharlene', 'Jodi', 'Allison', 'Wendy', 'Maya', 'Sarah', 'Penny', 'Jennifer']
    lname = ['Smith', 'West', 'Gray', 'Picoult', 'Bryce', 'Bautista', 'Minogue', 'Hernandez', 'Evans', 'Lopez', 'Faraon', 'Moore', 'Taylor', 'Khan']
    
    for memship in models.Membership.objects.filter(approved=True):
      for n in range(10):
        donor = models.Donor(membership=memship, firstname=fname[random.randint(0,15)], lastname=lname[random.randint(0,13)], amount = random.randint(1,500), likelihood=random.randint(1,100))
        donor.save()

    #steps - 1 per donor
    descs = ['Talk to about project', 'Ask', 'Invite to panel', 'Dinner', 'Coffee']
    for donor in models.Donor.objects.all():
      days = [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7]
      time = datetime.timedelta(days=days[random.randint(0, 10)])
      step = models.Step(donor=donor, complete=False, date=timezone.now()+time, description = descs[random.randint(0,4)])
      step.save()
      
  return redirect(Home)
  
def UpdateDB(request): #from django 1.3 -> 1.4, making stored datetimes aware

  tz = timezone.get_default_timezone()
  count = 0
  logging.info("Time zone conversion starting - using " + str(tz))
  
  cycles = models.GrantCycle.objects.all() #GrantCycle
  logging.info(str(cycles.count()) + ' grant cycle(s)')
  for cyc in cycles:
    logstr = str(cyc)
    if timezone.is_aware(cyc.open):
      logstr +=  ': .open is aware'
    else:
      count += 1
      logstr += ': .open changed from '+ str(cyc.open) + ' to ' + str(timezone.make_aware(cyc.open))
    if timezone.is_aware(cyc.close):
      logstr += '; .close is aware '
    else:
      count += 1
      logstr += '; .close '+ str(cyc.close) + ' to ' + str(timezone.make_aware(cyc.close))
    logging.info(logstr)
  
  drafts = grants.models.SavedGrantApplication.objects.all() #SavedGrantApplication
  logging.info(str(drafts.count()) + ' draft applications')
  for draft in drafts:
    logstr = str(draft)
    if timezone.is_aware(draft.modified):
      logstr +=  ': .modified is aware'
    else:
      count += 1
      logstr += ': .modified changed from '+ str(draft.modified) + ' to ' + str(timezone.make_aware(draft.modified))
    logging.info(logstr)
  
  apps = grants.models.GrantApplication.objects.all() #GrantApplication
  logging.info(str(apps.count()) + ' submitted applications')
  for app in apps:
    logstr = str(app)
    if timezone.is_aware(app.submission_time):
      logstr +=  ': .submission_time is aware'
    else:
      count += 1
      logstr += ': .submission_time changed from '+ str(app.submission_time) + ' to ' + str(timezone.make_aware(app.submission_time))
    logging.info(logstr)
  
  news = models.NewsItem.objects.all() #NewsItem
  logging.info(str(news.count()) + ' news posts')
  for new in news:
    logstr = str(new)
    if timezone.is_aware(new.date):
      logstr +=  ': .date is aware'
    else:
      count += 1
      logstr += ': .date changed from '+ str(new.date) + ' to ' + str(timezone.make_aware(new.date))
    logging.info(logstr)
    
  events = models.Event.objects.all() #Event
  logging.info(str(events.count()) + ' events')
  for event in events:
    logstr = str(event)
    if timezone.is_aware(event.date):
      logstr +=  ': .date is aware'
    else:
      count += 1
      logstr += ': .date changed from '+ str(event.date) + ' to ' + str(timezone.make_aware(event.date))
    logging.info(logstr)
  
  logging.info('Time zone conversion complete; ' + str(count) + ' fields updated.')
  
  return render_to_response('debug.html', {'tz':tz})
