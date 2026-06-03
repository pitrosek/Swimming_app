from django.contrib import admin
from .models import Stat, Mesto, Klub, Plavec, Trener, Disciplina, Zavod, DisciplinyZavodu, Vysledek


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('nazev', 'hymna')
    search_fields = ('nazev',)


@admin.register(Mesto)
class MestoAdmin(admin.ModelAdmin):
    list_display = ('nazev', 'stat')
    search_fields = ('nazev',)
    list_filter = ('stat',)


@admin.register(Klub)
class KlubAdmin(admin.ModelAdmin):
    list_display = ('nazev', 'mesto', 'datum_zalozeni')
    search_fields = ('nazev',)
    list_filter = ('mesto', 'datum_zalozeni')


@admin.register(Plavec)
class PlavecAdmin(admin.ModelAdmin):
    list_display = ('jmeno', 'prijmeni', 'rocnik', 'pohlavi', 'klub', 'stat')
    search_fields = ('jmeno', 'prijmeni')
    list_filter = ('pohlavi', 'klub', 'stat')
    fieldsets = (
        ('Osobní údaje', {
            'fields': ('jmeno', 'prijmeni', 'rocnik', 'pohlavi', 'foto')
        }),
        ('Fyzické parametry', {
            'fields': ('vaha', 'vyska')
        }),
        ('Členství', {
            'fields': ('klub', 'stat')
        }),
    )


@admin.register(Trener)
class TrenerAdmin(admin.ModelAdmin):
    list_display = ('jmeno', 'prijmeni', 'klub', 'stat')
    search_fields = ('jmeno', 'prijmeni')
    list_filter = ('klub', 'stat')
    filter_horizontal = ('plavci',)
    fieldsets = (
        ('Osobní údaje', {
            'fields': ('jmeno', 'prijmeni', 'pohlavi', 'foto')
        }),
        ('Členství', {
            'fields': ('klub', 'stat')
        }),
        ('Svěřenci', {
            'fields': ('plavci',)
        }),
    )


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nazev', 'delka', 'styl', 'pohlavi')
    search_fields = ('nazev',)
    list_filter = ('styl', 'pohlavi', 'delka')


@admin.register(Zavod)
class ZavodAdmin(admin.ModelAdmin):
    list_display = ('nazev', 'datum', 'cas_zahajeni', 'misto', 'bazen')
    search_fields = ('nazev', 'misto')
    list_filter = ('datum', 'bazen')


@admin.register(DisciplinyZavodu)
class DisciplinyZavoduAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'zavod', 'zacatek')
    search_fields = ('disciplina__nazev', 'zavod__nazev')
    list_filter = ('zavod', 'zacatek')


@admin.register(Vysledek)
class VysledekAdmin(admin.ModelAdmin):
    list_display = ('plavec', 'zavod', 'disciplina', 'umisteni', 'body')
    search_fields = ('plavec__jmeno', 'plavec__prijmeni', 'zavod__nazev')
    list_filter = ('zavod', 'disciplina', 'umisteni')

