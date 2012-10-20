from scoring.models import *
from django.contrib import admin
from fund.admin import advanced_admin
import logging

# Admin setup isn't required for this project, but in case it is helpful for testing:

""" 
  Basic vs. advanced:
    Advanced admin site is visible to developers only, not staff.  Anything that could cause errors if edited should be added to advanced only, or you should make a custom admin model to restrict editing.

  To add a model to the the basic admin:
    admin.site.register(Modelname)

  To add to the advanced admin:
    advanced_admin.register(Modelname)

  Customizing example - see https://docs.djangoproject.com/en/dev/ref/contrib/admin/
    class GranteeAdmin(admin.ModelAdmin):
      list_display = ('name', 'email',)
      list_editable = ('email',)
    
"""