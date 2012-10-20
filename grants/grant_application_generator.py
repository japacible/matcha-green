from django.core.management.base import BaseCommand, CommandError
from grants.models import generate_grantcycle
from grants.models import generate_grantee
from grants.models import GrantApplication
import random
import hashlib
import datetime

def generate_string():
    return hashlib.md5(str(random.uniform(0, 1))).hexdigest()

class Command(BaseCommand):

    def handle(self, *args, **options):
        b = GrantApplication()
        b.organization = generate_grantee()
        b.grant_cycle = generate_grantcycle()
        b.submission_time = datetime.date.today()
        b.address = generate_string()
        b.city = generate_string()
        b.state = random.choice(b.STATE_CHOICES)[0]
        b.zip = str(random.randrange(10000, 99999))
        b.telephone_number = "(" + str(random.randrange(100,1000)) + ")" + str(random.randrange(100, 1000)) + "-" + str(random.randrange(1000,10000))
        b.fax_number = "(" + str(random.randrange(100,1000)) + ")" + str(random.randrange(100, 1000)) + "-" + str(random.randrange(1000,10000))
        b.email_address = generate_string() + "@gmail.com"
        b.website = generate_string() + ".org"
        b.status = random.choice(a.STATUS_CHOICES)[0]
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
        b.fiscal_telephone = generate_string()
        b.fiscal_email = generate_string()
        b.fiscal_address = generate_string()
        b.fiscal_letter = generate_string()
        b.fiscal_letter_name = generate_string()
        b.fiscal_letter_type = generate_string()
        b.screening_status = random.choice(b.SCREENING_CHOICES)[0]
        b.scoring_bonus_poc = TRUE
        b.scoring_bonus_geo = TRUE


