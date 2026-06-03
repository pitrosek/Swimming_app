from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Uživatelský profil s rolí (plavec nebo trenér)"""
    
    ROLE_CHOICES = [
        ('plavec', 'Plavec'),
        ('trener', 'Trenér'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_profile'
        verbose_name = 'Uživatelský Profil'
        verbose_name_plural = 'Uživatelské Profily'
    
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class Stat(models.Model):

    stat_id = models.AutoField(primary_key=True)
    nazev = models.CharField(max_length=4, unique=True)  # CZE, SVK, POL, GER, UKR
    hymna = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'stat'
        verbose_name = 'Stát'
        verbose_name_plural = 'Státy'

    def __str__(self):
        return self.nazev


class Mesto(models.Model):
    
    mesto_id = models.AutoField(primary_key=True)
    nazev = models.CharField(max_length=100)
    symbol = models.BinaryField(blank=True, null=True)
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE)

    class Meta:
        db_table = 'mesto'
        verbose_name = 'Město'
        verbose_name_plural = 'Města'

    def __str__(self):
        return f"{self.nazev} ({self.stat.nazev})"


class Klub(models.Model):
    
    klub_id = models.AutoField(primary_key=True)
    nazev = models.CharField(max_length=100)
    mesto = models.ForeignKey(Mesto, on_delete=models.CASCADE)
    datum_zalozeni = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'klub'
        verbose_name = 'Klub'
        verbose_name_plural = 'Kluby'

    def __str__(self):
        return self.nazev


class Plavec(models.Model):
   
    POHLAVI_CHOICES = [
        ('M', 'Muž'),
        ('Z', 'Žena'),
    ]

    plavec_id = models.AutoField(primary_key=True)
    jmeno = models.CharField(max_length=100)
    prijmeni = models.CharField(max_length=100)
    rocnik = models.IntegerField()  # Rok narození
    vaha = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    vyska = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pohlavi = models.CharField(max_length=1, choices=POHLAVI_CHOICES)
    foto = models.CharField(max_length=255, blank=True, null=True)
    klub = models.ForeignKey(Klub, on_delete=models.SET_NULL, null=True)
    stat = models.ForeignKey(Stat, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'plavec'
        verbose_name = 'Plavec'
        verbose_name_plural = 'Plavci'

    def __str__(self):
        return f"{self.jmeno} {self.prijmeni}"


class Trener(models.Model):
    
    POHLAVI_CHOICES = [
        ('M', 'Muž'),
        ('Z', 'Žena'),
    ]

    trener_id = models.AutoField(primary_key=True)
    jmeno = models.CharField(max_length=100)
    prijmeni = models.CharField(max_length=100)
    pohlavi = models.CharField(max_length=1, choices=POHLAVI_CHOICES, blank=True, null=True)
    foto = models.CharField(max_length=255, blank=True, null=True)
    klub = models.ForeignKey(Klub, on_delete=models.SET_NULL, null=True)
    stat = models.ForeignKey(Stat, on_delete=models.SET_NULL, null=True)
    plavci = models.ManyToManyField(Plavec, related_name='treneri', blank=True)

    class Meta:
        db_table = 'trener'
        verbose_name = 'Trenér'
        verbose_name_plural = 'Trenéři'

    def __str__(self):
        return f"{self.jmeno} {self.prijmeni}"


class Disciplina(models.Model):
   
    STYL_CHOICES = [
        ('volný způsob', 'Volný způsob'),
        ('prsa', 'Prsa'),
        ('motýl', 'Motýl'),
        ('znak', 'Znak'),
        ('polohový závod', 'Polohový závod'),
    ]
    POHLAVI_CHOICES = [
        ('M', 'Muž'),
        ('Z', 'Žena'),
    ]

    disciplina_id = models.AutoField(primary_key=True)
    nazev = models.CharField(max_length=100)
    delka = models.IntegerField(validators=[MinValueValidator(1)])  # délka v metrech
    styl = models.CharField(max_length=20, choices=STYL_CHOICES)
    pohlavi = models.CharField(max_length=1, choices=POHLAVI_CHOICES)

    class Meta:
        db_table = 'disciplina'
        verbose_name = 'Disciplína'
        verbose_name_plural = 'Disciplíny'
        unique_together = ('styl', 'pohlavi', 'delka')

    def __str__(self):
        return self.nazev


class Zavod(models.Model):
    
    BAZEN_CHOICES = [
        ('50', '50 metrů'),
        ('25', '25 metrů'),
    ]

    zavod_id = models.AutoField(primary_key=True)
    nazev = models.CharField(max_length=100)
    datum = models.DateField(blank=True, null=True)
    cas_zahajeni = models.TimeField(blank=True, null=True)
    misto = models.CharField(max_length=20)
    bazen = models.CharField(max_length=2, choices=BAZEN_CHOICES)

    class Meta:
        db_table = 'zavod'
        verbose_name = 'Závod'
        verbose_name_plural = 'Závody'

    def __str__(self):
        return self.nazev


class DisciplinyZavodu(models.Model):
   
    discipliny_zavodu_id = models.AutoField(primary_key=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    zavod = models.ForeignKey(Zavod, on_delete=models.CASCADE)
    zacatek = models.TimeField()

    class Meta:
        db_table = 'discipliny_zavodu'
        verbose_name = 'Disciplína závodu'
        verbose_name_plural = 'Disciplíny závodu'
        unique_together = ('disciplina', 'zavod')

    def __str__(self):
        return f"{self.disciplina.nazev} - {self.zavod.nazev}"


class Vysledek(models.Model):
    
    vysledek_id = models.AutoField(primary_key=True)
    zavod = models.ForeignKey(Zavod, on_delete=models.CASCADE)
    plavec = models.ForeignKey(Plavec, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    umisteni = models.IntegerField(validators=[MinValueValidator(1)])
    cas = models.IntegerField(blank=True, null=True, help_text="Čas v sekundách")
    body = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'vysledek'
        verbose_name = 'Výsledek'
        verbose_name_plural = 'Výsledky'

    def __str__(self):
        return f"{self.plavec} - {self.disciplina} ({self.umisteni}. místo)"

