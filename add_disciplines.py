#!/usr/bin/env python
import os
import django
from datetime import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plavecke_zavody.settings')
django.setup()

from zavody.models import Zavod, DisciplinyZavodu, Disciplina

# Get the future competition
zavod = Zavod.objects.get(zavod_id=3)

# Get all disciplines
discipliny = Disciplina.objects.all()

# Add all disciplines to the competition with staggered start times
start_time = time(10, 0)  # 10:00 AM
for idx, disciplina in enumerate(discipliny):
    if not DisciplinyZavodu.objects.filter(zavod=zavod, disciplina=disciplina).exists():
        # Calculate start time: add 30 minutes for each discipline
        hour = 10 + (idx * 30) // 60
        minute = (idx * 30) % 60
        dz_time = time(hour, minute)
        
        DisciplinyZavodu.objects.create(zavod=zavod, disciplina=disciplina, zacatek=dz_time)
        print(f"Disciplína {disciplina.nazev} přidána na závod {zavod.nazev} na {dz_time}")

print(f"\nCelkem {discipliny.count()} disciplín přidáno!")
