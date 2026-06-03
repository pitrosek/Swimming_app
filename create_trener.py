#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plavecke_zavody.settings')
django.setup()

from zavody.models import Trener, Klub, Stat
from django.contrib.auth.models import User

# Get David user
user = User.objects.get(username='david_kouc')

# Create Trener for David with a club and stat
klub = Klub.objects.first()  # Get first club
stat = Stat.objects.first()  # Get first stat

trener = Trener.objects.create(
    jmeno='David',
    prijmeni='Kouč',
    pohlavi='M',
    klub=klub,
    stat=stat
)

print(f"Trenér {trener.jmeno} {trener.prijmeni} vytvořen!")
