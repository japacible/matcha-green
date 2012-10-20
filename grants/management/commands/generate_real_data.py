from django.core.management.base import BaseCommand, CommandError
from grants.models import GrantApplication
from grants.models import GrantCycle
from grants.models import Grantee


import datetime

def generate_grantee():
    a = Grantee()
    a.name  = "Adeptus Mechanicus"
    a.email = "adMech@gmail.com"
    a.city = "Seattle"
    a.state = "WA"
    a.zip = 98020
    a.telephone_number = "(206)-275-8291"
    a.email_address = "adeptusMechanicus@gmail.com"
    a.website = "adMech.org"
    a.status = 'Tribal government'
    a.save()
    return a

def generate_grantcycle():
	c = GrantCycle()
	c.open  = datetime.datetime(2003, 8, 4, 12, 30, 45)
	c.close = datetime.datetime(2003, 8, 4, 12, 30, 45)
	c.save()
	return c


class Command(BaseCommand):

    def handle(self, *args, **options):
        b = GrantApplication()
        b.grant_cycle = generate_grantcycle()
        b.organization = generate_grantee()
        b.submission_time = datetime.datetime(2003, 8, 4, 12, 30, 45)
        b.address = "8283 37st NW"
        b.city = 'Seattle'
        b.state = 'WA'
        b.zip = 90210
        b.telephone_number = "(201)626-1029"
        b.email_address = "adMech@gmail.com"
        b.status = 'Tribal government'
        b.ein = 123-4567890
        b.founded = 1996
        b.contact_person = "Ollanius Pius"
        b.amount_requested = 28989928
        b.support_type = 'General support'
        b.project_title = "title1"
        
        b.grant_period = "Fall"
        b.start_year = 1996
        b.budget_last = 10000
        b.budget_current = 100000
        
        b.screening_status = 80
        b.scoring_bonus_poc = True
        b.scoring_bonus_geo = True
        b.save()