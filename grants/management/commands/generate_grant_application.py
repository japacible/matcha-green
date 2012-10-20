from django.core.management.base import BaseCommand, CommandError
from grants.models import *
import random
import hashlib
import datetime

def generate_string():
    return hashlib.md5(str(random.uniform(0, 1))).hexdigest()

def generate_grant_application():
    b = GrantApplication()
    b.organization = Grantee.objects.order_by('?')[0]
    b.grant_cycle = GrantCycle.objects.order_by('?')[0]

    b.submission_time = datetime.date.today()
    b.address = generate_string()
    b.city = generate_string()
    b.state = random.choice(b.STATE_CHOICES)[0]
    b.zip = str(random.randrange(10000, 99999))
    b.telephone_number = "(" + str(random.randrange(100,1000)) + ")" + str(random.randrange(100, 1000)) + "-" + str(random.randrange(1000,10000))
    b.fax_number = "(" + str(random.randrange(100,1000)) + ")" + str(random.randrange(100, 1000)) + "-" + str(random.randrange(1000,10000))
    b.email_address = generate_string() + "@gmail.com"
    b.website = generate_string() + ".org"
    b.status = random.choice(b.STATUS_CHOICES)[0]
    b.ein = str(random.randrange(10,100)) + "-" + str(random.randrange(1000000,100000000))
    b.founded = random.randrange(1800, 2013)
    b.mission = generate_string()
    b.contact_person = generate_string() + " " + generate_string()
    b.amount_requested = random.randrange(0,100000000)
    b.support_type = random.choice(b.SUPPORT_CHOICES)[0]
    b.grant_period = generate_string()
    b.start_year = generate_string()
    b.budget_last = random.randrange(0,100000000)
    b.budget_current = random.randrange(0,100000000)
    b.project_title = generate_string()
    b.project_budget = random.randrange(0,100000000)
    b.grant_request = generate_string()
    b.previous_grants = generate_string()
    b.fiscal_org = generate_string()
    b.fiscal_person = generate_string()
    b.fiscal_telephone = '911'
    b.fiscal_email = generate_string()
    b.fiscal_address = generate_string()
    b.fiscal_letter = generate_string()
    b.fiscal_letter_name = generate_string()
    b.fiscal_letter_type = 'wut'
    b.screening_status = random.choice(b.SCREENING_CHOICES)[0]
    b.scoring_bonus_poc = True
    b.scoring_bonus_geo = True
    return b;


class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) != 1:
            print "Usage: python manage.py generate_grant_application n"
            print "Saves n grant applications"
        else:
            times = int(args[0])
            for times in range(0, times):
                grant_app = generate_grant_application()
                grant_app.save()
