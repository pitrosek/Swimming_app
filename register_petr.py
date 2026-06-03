#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plavecke_zavody.settings')
django.setup()

from zavody.models import Vysledek, Plavec, Zavod

# Delete all registrations for Petr Vítek on the future competition if they exist
plavec = Plavec.objects.get(plavec_id=1)  # Petr Vítek
zavod = Zavod.objects.get(zavod_id=3)  # Budoucí Velká cena

vysledky = Vysledek.objects.filter(zavod=zavod, plavec=plavec)
count = vysledky.count()
vysledky.delete()

if count > 0:
    print(f"Vymazáno {count} záznamů")
else:
    print("Žádné záznamy k vymazání")

# Now recreate the registrations for Petr with the disciplines
from zavody.models import DisciplinyZavodu

discipliny_zavodu = DisciplinyZavodu.objects.filter(zavod=zavod)
print(f"\nVytvářím registraci pro {plavec.jmeno} na {discipliny_zavodu.count()} disciplín:")

for dz in discipliny_zavodu:
    vysledek = Vysledek.objects.create(
        zavod=zavod,
        plavec=plavec,
        disciplina=dz.disciplina,
        umisteni=999  # Placeholder
    )
    print(f"  - Vytvořeno: {vysledek.disciplina.nazev}")

print(f"\nCelkem {discipliny_zavodu.count()} registrací vytvořeno!")
