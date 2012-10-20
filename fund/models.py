from django import forms
from django.db import models
from django.forms import ModelForm
import datetime
from grants.models import GrantCycle
from django.utils import timezone

class GivingProject(models.Model):
  title = models.CharField(max_length=255)

  #fundraising
  fundraising_deadline = models.DateField(help_text='Members will stop receiving reminder emails at this date.')
  fund_goal = models.PositiveIntegerField(default=0)
  pre_approved = models.TextField(null=True, blank=True, help_text='List of member emails, separated by commas.  Anyone who registers using an email on this list will have their account automatically approved.  Emails are removed from the list once they have registered.  IMPORTANT: Any syntax error can make this feature stop working; in that case memberships will default to requiring manual approval by an administrator.') #remove null from all char
  
  calendar = models.CharField(max_length=255, null=True, blank=True, help_text= 'Calendar ID of a google calendar (not the whole embed text)')
  r1title = models.CharField(verbose_name='Resource title', max_length=255, null=True, blank=True)
  r1link= models.URLField(verbose_name='Resource link', null=True, blank=True)
  r2title = models.CharField(verbose_name='Resource title', max_length=255, null=True, blank=True)
  r2link= models.URLField(verbose_name='Resource link', null=True, blank=True)
  r3title = models.CharField(verbose_name='Resource title', max_length=255, null=True, blank=True)
  r3link= models.URLField(verbose_name='Resource link', null=True, blank=True)
  r4title = models.CharField(verbose_name='Resource title', max_length=255, null=True, blank=True)
  r4link= models.URLField(verbose_name='Resource link', null=True, blank=True)
  r5title = models.CharField(verbose_name='Resource title', max_length=255, null=True, blank=True)
  r5link= models.URLField(verbose_name='Resource link', null=True, blank=True)
  r6title = models.CharField(verbose_name='Resource title', max_length=255, null=True, blank=True)
  r6link= models.URLField(verbose_name='Resource link', null=True, blank=True)
  r7title = models.CharField(verbose_name='Resource title', max_length=255, null=True, blank=True)
  r7link= models.URLField(verbose_name='Resource link', null=True, blank=True)
  r8title = models.CharField(verbose_name='Resource title', max_length=255, null=True, blank=True)
  r8link= models.URLField(verbose_name='Resource link', null=True, blank=True)
  r9title = models.CharField(verbose_name='Resource title', max_length=255, null=True, blank=True)
  r9link= models.URLField(verbose_name='Resource link', null=True, blank=True)
  r10title = models.CharField(verbose_name='Resource title', max_length=255, null=True, blank=True)
  r10link= models.URLField(verbose_name='Resource link', null=True, blank=True)

  #grant
  grant_cycle = models.ForeignKey(GrantCycle, null=True, blank=True)

  def __unicode__(self):
    return self.title+' '+str(self.fundraising_deadline.year)

  def talked(self):
    return Donor.objects.filter(membership__giving_project=self, talked=True).count()

  def asked(self):
    return Donor.objects.filter(membership__giving_project=self, asked=True).count()

  def contacts(self):
    return Donor.objects.filter(membership__giving_project=self).count()

  def pledged(self):
    donors = Donor.objects.filter(membership__giving_project=self)
    pledged = 0
    for donor in donors:
      if donor.pledged:
        pledged = pledged + donor.pledged
    return pledged

  def bar_width(self):
    if self.fund_goal>0:
      pl = self.pledged()
      if pl>self.fund_goal:
        return 100
      else:
        return 100*pl/self.fund_goal
    else:
      return 0

  def gifted(self):
    donors = Donor.objects.filter(membership__giving_project=self, gifted__gt=0)
    gifted = 0
    for donor in donors:
      gifted = gifted + donor.gifted()
    return gifted

  def estimated(self):
    estimated = 0
    donors = Donor.objects.filter(membership__giving_project=self)
    for donor in donors:
      estimated = estimated + donor.amount*donor.likelihood/100
    return estimated
    
class Member(models.Model):
  email = models.CharField(max_length=255)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  
  giving_project = models.ManyToManyField(GivingProject, through='Membership')
  current = models.IntegerField(default=0)
  
  def __unicode__(self):
    return self.first_name+' '+self.last_name
  
class Membership(models.Model): #relationship b/n member and gp
  giving_project = models.ForeignKey(GivingProject)
  member = models.ForeignKey(Member)
  approved = models.BooleanField(default=False)
  leader = models.BooleanField(default=False)
  
  emailed = models.DateField(default='2000-01-01', help_text='Last time this member was sent an overdue steps reminder')
  last_activity = models.DateField(default='2000-01-01', help_text='Last activity by this user on this membership.')
  
  notifications = models.TextField(default='', blank=True)
  
  def __unicode__(self):
    return str(self.member)+', '+str(self.giving_project)
    
  def has_overdue(self):
    donors = self.donor_set.all()
    overdue = 0
    day = datetime.timedelta(days=1)
    for donor in donors:
      if donor.has_overdue() and donor.has_overdue()>day: #1 day grace period to member to update
        overdue = overdue+1
    return overdue

  def talked(self):
    return self.donor_set.filter(talked=True).count()

  def asked(self):
    return self.donor_set.filter(asked=True).count()

  def bar_width(self):
    if self.donor_set.count()>0:
      return 100*self.asked()/self.donor_set.count()
    else:
      return 0
        
  def pledged(self):
    donors = self.donor_set.all()
    amt = 0
    for donor in donors:
      if donor.pledged:
        amt = amt + donor.pledged
    return amt
  
  def gifted(self):
    donors = self.donor_set.all()
    amt = 0
    for donor in donors:
      amt = amt + donor.gifted
    return amt

  def estimated(self):
    estimated = 0
    donors = self.donor_set.all()
    for donor in donors:
      estimated = estimated + donor.amount*donor.likelihood/100
    return estimated

class Donor(models.Model):
  membership = models.ForeignKey(Membership)
  
  firstname = models.CharField(max_length=100, verbose_name='*First name')
  lastname = models.CharField(max_length=100, null=True, blank=True, verbose_name='Last name')
  PRIVACY_CHOICES = (
    ('PR', 'Private - cannot be seen by staff'),
    ('SH', 'Shared'),
  )
  privacy = models.CharField(max_length=2, choices=PRIVACY_CHOICES, default='SH')
  amount = models.PositiveIntegerField(verbose_name='*Amount to ask ($)')
  likelihood = models.PositiveIntegerField(verbose_name='*Estimated likelihood (%)')
  talked = models.BooleanField(default=False)
  asked = models.BooleanField(default=False)
  pledged = models.PositiveIntegerField(blank=True, null=True)
  gifted = models.PositiveIntegerField(default=0)
  gift_notified = models.BooleanField(default=False)
  phone = models.CharField(max_length=15, null=True, blank=True)
  email = models.EmailField(null=True, blank=True)
  
  def __unicode__(self):
    return self.firstname+' '+self.lastname
  
  def get_next_step(self):
    step = Step.objects.filter(donor=self, complete=False)
    if step:
      return step[0]
    else:
      return None
  
  def get_next_date(self): #used to sort donors
    step = Step.objects.filter(donor=self, complete=False)
    
    if step: #next step - top
      return step[0].date
    elif self.pledged: # 'done' - all the way to bottom
      return timezone.now().date()+datetime.timedelta(weeks=100)
    else: #no step, not done - middle
      return timezone.now().date()+datetime.timedelta(weeks=70)
    
  def get_steps(self): #used in expanded view
    return Step.objects.filter(donor=self).filter(complete=True).order_by('date')
  
  def has_overdue(self):
    steps = Step.objects.filter(donor=self, complete=False)
    for step in steps:
      if step.date < timezone.now().date():
        return timezone.now().date()-step.date
    return False
  
def make_custom_datefield(f):
  """date selector implementation from http://strattonbrazil.blogspot.com/2011/03/using-jquery-uis-date-picker-on-all.html """
  formfield = f.formfield()
  if isinstance(f, models.DateField):
      formfield.widget.format = '%m/%d/%Y'
      formfield.widget.attrs.update({'class':'datePicker', 'readonly':'true'})
  return formfield
    
class DonorForm(ModelForm): #used to edit, creation uses custom form
  class Meta:
    model = Donor
    fields = ('firstname', 'lastname', 'amount', 'likelihood', 'phone', 'email', 'asked', 'pledged')

class Step(models.Model):  
  date = models.DateField(verbose_name='Date')
  description = models.CharField(max_length=255, verbose_name='Description')
  donor = models.ForeignKey(Donor)
  complete = models.BooleanField(default=False)

  def __unicode__(self):
    return self.date.strftime('%m/%d/%y')+' '+self.description
    
class StepForm(ModelForm):
  formfield_callback = make_custom_datefield #date input
  
  class Meta:
    model = Step
    exclude = ('donor', 'complete')
    
class NewsItem(models.Model):
  date = models.DateTimeField(auto_now=True)
  project = models.ForeignKey(GivingProject)
  short = models.CharField(max_length=255, help_text='News summary that shows in the news box.')
  long = models.TextField(null=True, blank=True, help_text='(Optional) Longer text to display on the news page.')
  title = models.CharField(max_length=255, null=True, blank=True, help_text='If including a long text, also include a title for the news page display.')
  link = models.URLField(null=True, blank=True, help_text='Displayed with the text "Read more" after the text on the news page.')
  def __unicode__(self):
    return self.short

class Event(models.Model):
  desc = models.CharField(max_length=255)
  date = models.DateTimeField()
  project = models.ForeignKey(GivingProject)
  location = models.CharField(max_length=255, null=True, blank=True)
  link = models.URLField(null=True, blank=True)
  def __unicode__(self):
    return self.desc