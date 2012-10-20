from django.core.management.base import BaseCommand, CommandError
from grants.models import GrantApplication
from grants.models import GrantCycle
from grants.models import Grantee


import datetime
from django.core.management.base import BaseCommand, CommandError
from grants.models import GrantApplication
from grants.models import GrantCycle
from grants.models import Grantee


import datetime

def generate_grantee():
    a = Grantee()
    a.name  = "Bill and Melinda Gates Foundation"
    a.email = "BMGF@gmail.com"
    a.city = "Cheyenne"
    a.state = "WY"
    a.zip = 10562
    a.telephone_number = "(800)-1828-1299"
    a.email_address = "BillAndMelindaGatesFoundation@gmail.com"
    a.website = "BillAndMelindaGatesFoundation.com"
    a.status = 'Sponsored'
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
        b.address = "8888 88th PL"
        b.city = 'Cheyenne'
        b.state = 'WY'
        b.zip = 38490
        b.telephone_number = "(222)377-2173"
        b.email_address = "BMGF@gmail.com"
        b.status = 'Sponsored'
        b.ein = 888-4572934
        b.founded = 2005
        b.contact_person = "Bill Gates"
        b.amount_requested = 28989928
        b.support_type = 'General support'
        b.project_title = "A better tomorrow"
        
        b.mission = "LGBTQ Giving Project"

        
        b.grant_period = "Spring"
        b.start_year = 2005
        b.budget_last = 1000000
        b.budget_current = 100000004
        
        b.screening_status = 30
        b.scoring_bonus_poc = False
        b.scoring_bonus_geo = False
        b.save()