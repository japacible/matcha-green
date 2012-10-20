from django.core.management.base import BaseCommand, CommandError
from grants.models import generate_grantcycle
from grants.models import generate_grantee
from grants.models import GrantApplication
from grants.models import GrantCycle
from grants.models import GrantApplication


import datetime

class Command(BaseCommand):

    def handle(self, *args, **options):
        a = Grantee()
        a.name  = "Children's Hospital"
        a.email = "childHosp@gmail.com"
        a.city = "Kent"
        a.state = "ID"
        a.zip = 99040
        a.telephone_number = "(276)-215-8231"
        a.email_address = "childHosp@gmail.com"
        a.website = "ChildrenHospital.org"
        a.status = 'Tribal government'
        a.save()

	def generate_grantcycle():
		c = GrantCycle()
		c.open  = datetime.datetime.now()
		c.close = datetime.datetime.now()
        c.save()

    def handle(self, *args, **options):
        b = GrantApplication()
        b.grant_cycle = c
        b.organization = a
        b.submission_time = datetime.date.today()
        b.address = "1234 28th ST"
        b.city = 'Kent'
        b.state = 'ID'
        b.zip = 99040
        b.telephone_number = "(201)623-1019"
        b.email_address = "Childrenhospital@gmail.com"
        b.status = 'Tribal government'
        b.ein = 123-4267190
        b.founded = 1985
        b.contact_person = "Moody"
        b.amount_requested = 1928382
        b.support_type = 'General support'
        b.project_title = "title1"
        
        b.grant_period = generate_string()
        b.start_year = 1996
        b.budget_last = 10000
        b.budget_current = 100000
        
        b.screening_status = 80
        b.scoring_bonus_poc = False
        b.scoring_bonus_geo = False
        b.save()