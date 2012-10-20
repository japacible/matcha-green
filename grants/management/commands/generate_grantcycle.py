from django.core.management.base import BaseCommand, CommandError

from grants.models import GrantCycle
import random
import datetime
import hashlib

def generate_string():
    return hashlib.md5(str(random.uniform(0, 1))).hexdigest()

def generate_grantcycle():
    a = GrantCycle()
    a.title = generate_string()
    a.open  = datetime.datetime.now()
    a.close = datetime.datetime.now()
    a.addition = generate_string()
    a.narrative = generate_string()
    return a

class Command(BaseCommand):

    def handle(self, *args, **options):
        if len(args) != 1:
            print "Usage: python manage.py generate_grantcycle n"
            print "Saves n grantcycles"
        else:
            times = int(args[0])
            for times in range(0, times):
                grantcycle = generate_grantcycle()
                grantcycle.save()
