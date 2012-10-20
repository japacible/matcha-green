from django.core.management.base import BaseCommand, CommandError

from grants.models import Grantee
import random
import hashlib

def generate_string():
    return hashlib.md5(str(random.uniform(0, 1))).hexdigest()

class Command(BaseCommand):

    def handle(self, *args, **options):
        a = Grantee()
        a.name  = generate_string()
        a.email = generate_string() + "@gmail.com"
        a.address = generate_string()
        a.city = generate_string()
        a.state = random.choice(a.STATE_CHOICES)[0]
        a.zip = str(random.randrange(10000, 99999))
        a.telephone_number = "(" + str(random.randrange(100,1000)) + ")" + str(random.randrange(100, 1000)) + "-" + str(random.randrange(1000,10000))
        a.fax_number = "(" + str(random.randrange(100,1000)) + ")" + str(random.randrange(100, 1000)) + "-" + str(random.randrange(1000,10000))
        a.email_address = generate_string() + "@gmail.com"
        a.website = generate_string() + ".org"
        a.status = random.choice(a.STATUS_CHOICES)[0]
        a.ein = str(random.randrange(10,100)) + "-" + str(random.randrange(1000000,100000000))
        a.founded = random.randrange(1800, 2013)
        a.mission_statement = generate_string()
        a.fiscal_org = generate_string()
        a.fiscal_person = generate_string()
        a.fiscal_telephone = "(" + str(random.randrange(100,1000)) + ")" + str(random.randrange(100, 1000)) + "-" + str(random.randrange(1000,10000))
        a.fiscal_email =  generate_string() + "@yahoo.com"
        a.fiscal_address =  generate_string()
        a.fiscal_letter = generate_string()
        a.fiscal_letterName = generate_string()
        a.fiscal_letter_type = str(random.randrange(0, 4))
        a.save()
