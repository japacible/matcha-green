from django.core.management.base import BaseCommand, CommandError
from grants.models import GrantApplication
from grants.models import GrantCycle
from grants.models import Grantee


import datetime

def generate_grantee():
    a = Grantee()
    a.name  = "Childrens Hospital"
    a.email = "ChildrensHospital@gmail.com"
    a.city = "Portland"
    a.state = "OR"
    a.zip = 83020
    a.telephone_number = "(222)-347-1299"
    a.email_address = "CHospital@gmail.com"
    a.website = "ChildrensHospital.com"
    a.status = '501c3'
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
        b.city = 'Portland'
        b.state = 'OR'
        b.zip = 83020
        b.telephone_number = "(223)474-1203"
        b.email_address = "ChildrensHospital@gmail.com"
        b.status = 'Tribal government'
        b.ein = 123-4567890
        b.founded = 1996
        b.contact_person = "Dr. Sean"
        b.amount_requested = 28989928
        b.support_type = 'General support'
        b.project_title = "title1"
        b.mission = "Next Generation Giving Project"
        
        b.grant_period = "Fall"
        b.start_year = 1987
        b.budget_last = 10000
        b.budget_current = 1000004
        
        b.screening_status = 10
        b.scoring_bonus_poc = False
        b.scoring_bonus_geo = False
        b.save()