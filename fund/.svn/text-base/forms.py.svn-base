from django import forms
import models, datetime
from django.utils import timezone

class LoginForm(forms.Form):
  email = forms.EmailField()
  password = forms.CharField(widget=forms.PasswordInput())

class RegistrationForm(forms.Form):
  first_name = forms.CharField(max_length=100)
  last_name = forms.CharField(max_length=100)
  email = forms.EmailField()
  password = forms.CharField(widget=forms.PasswordInput())
  giving_project = forms.ModelChoiceField(queryset=models.GivingProject.objects.filter(fundraising_deadline__gte=timezone.now().date()), empty_label="Select a giving project", required=False)

class AddProjectForm(forms.Form):
  giving_project = forms.ModelChoiceField(queryset=models.GivingProject.objects.filter(fundraising_deadline__gte=timezone.now().date()), empty_label="Select a giving project")

class NewDonor(forms.Form):
  firstname = forms.CharField(max_length=100, label='*First name')
  lastname = forms.CharField(max_length=100, required=False, label='Last name')
  amount = forms.IntegerField(label='*Estimated donation ($)')
  likelihood = forms.IntegerField(label='*Estimated likelihood (%)')
  phone = forms.CharField(max_length=15,required=False)
  email = forms.EmailField(required=False)

  step_date = forms.DateField(required=False, label='Date', widget=forms.DateInput(attrs={'class':'datePicker', 'readonly':'true'}, format='%Y-%m-%d'))
  step_desc = forms.CharField(required=False, max_length=255, label='Description')

class MassDonor(forms.Form):
  firstname = forms.CharField(max_length=100, label='*First name')
  lastname = forms.CharField(max_length=100, required=False, label='Last name')
  amount = forms.IntegerField(label='*Estimated donation ($)', widget=forms.TextInput(attrs={'class':'tq'}))
  likelihood = forms.IntegerField(label='*Estimated likelihood (%)', widget=forms.TextInput(attrs={'class':'half'}))

class MassStep(forms.Form):
  date = forms.DateField(widget=forms.DateInput(attrs={'class':'datePicker', 'readonly':'true'}, format='%Y-%m-%d'), required=False)
  description = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'onfocus':'showSuggestions(this.id)'}))
  donor = forms.ModelChoiceField(queryset=models.Donor.objects.all(), widget=forms.HiddenInput())
  
  def clean(self):
    cleaned_data = super(MassStep, self).clean()
    date = cleaned_data.get("date")
    desc = cleaned_data.get("description")
    msg = "This field is required."
    if date:
      if not desc: #date, no desc - invalid
        self._errors["description"] = self.error_class([msg])
        del cleaned_data["description"]
    elif desc: # desc, no date - invalid
      self._errors["date"] = self.error_class([msg])
      del cleaned_data["date"]
    else: #neither - valid, but not wanted in data
      cleaned_data = []
    return cleaned_data
  
class StepDoneForm(forms.Form):
  asked = forms.BooleanField(required=False)
  #widget=forms.CheckboxInput(attrs={'onclick':'toggleAsk()'}))
  pledged_amount = forms.IntegerField(required=False)
  #share = forms.BooleanField(required=False, initial=True)
  next_step = forms.CharField(max_length=100, required=False)
  next_step_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class':'datePicker', 'readonly':'true'}, format='%m/%d/%Y'))
