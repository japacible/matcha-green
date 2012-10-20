from grants.models import *
from fund.models import *
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
  
      ## GRANTS ##

class GrantAppAdmin(admin.ModelAdmin):
  fields = ('screening_status', 'grant_cycle', 'scoring_bonus_poc', 'scoring_bonus_geo', 'file1', 'file1_name', 'file1_type')
  list_display = ('organization', 'submission_time', 'screening_status')  

class DraftAdmin(admin.ModelAdmin):
  list_display = ('organization', 'grant_cycle', 'modified')

class GranteeAdmin(admin.ModelAdmin):
  list_display = ('name', 'email',)
  list_editable = ('email',)

from fund.admin import advanced_admin

advanced_admin.register(GrantCycle)
advanced_admin.register(NarrativeText)
advanced_admin.register(Grantee, GranteeAdmin)
advanced_admin.register(GrantApplication, GrantAppAdmin)
advanced_admin.register(SavedGrantApplication, DraftAdmin)