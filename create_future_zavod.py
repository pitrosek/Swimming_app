#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plavecke_zavody.settings')
django.setup()

from zavody.models import Zavod

# Create a future competition (30 days from now)
future_date = datetime.now() + timedelta(days=30)

zavod = Zavod.objects.create(
    nazev='Budoucí Velká cena',
    datum=future_date.date(),
    cas_zahajeni='10:00:00',
    misto='Praha',
    bazen='50'  # Use the choice value, not the display text
)

print(f"Závod '{zavod.nazev}' vytvořen na datum {zavod.datum}!")

