#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plavecke_zavody.settings')
django.setup()

from zavody.models import Vysledek, Plavec, Zavod

# Check if Petr Vítek is registered on the future competition
plavec = Plavec.objects.get(plavec_id=1)  # Petr Vítek
zavod = Zavod.objects.get(zavod_id=3)  # Budoucí Velká cena

vysledky = Vysledek.objects.filter(zavod=zavod, plavec=plavec)
print(f"Počet registrací pro {plavec.jmeno} na závod {zavod.nazev}: {vysledky.count()}")

for vysledek in vysledky:
    print(f"  - {vysledek.disciplina.nazev}: umístění {vysledek.umisteni}")
