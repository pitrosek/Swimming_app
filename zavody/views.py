from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Zavod, Plavec, Klub, Stat, Vysledek, Disciplina, DisciplinyZavodu, Trener

# Domovská stránka
def home(request):
    zavody = Zavod.objects.all().order_by('-datum')[:6]
    plavci_count = Plavec.objects.count()
    kluby_count = Klub.objects.count()
    zavody_count = Zavod.objects.count()
    stavy_count = Stat.objects.count()
    
    context = {
        'zavody': zavody,
        'plavci_count': plavci_count,
        'kluby_count': kluby_count,
        'zavody_count': zavody_count,
        'stavy_count': stavy_count,
    }
    return render(request, 'zavody/home.html', context)

# Seznam všech závodů
def zavody_list(request):
    from datetime import datetime
    today = datetime.now().date()
    
    # Všechny závody seřazené podle data
    zavody_all = Zavod.objects.all().order_by('-datum')
    
    # Vyhledávání
    query = request.GET.get('q')
    if query:
        zavody_all = zavody_all.filter(Q(nazev__icontains=query) | Q(misto__icontains=query))
    
    # Rozdělení na nadcházející a proběhlé
    nadchazejici = zavody_all.filter(datum__gte=today)
    probehlé = zavody_all.filter(datum__lt=today)
    
    context = {
        'nadchazejici': nadchazejici,
        'probehlé': probehlé,
        'query': query
    }
    return render(request, 'zavody/zavody_list.html', context)

# Detail závodu
def zavod_detail(request, pk):
    from datetime import datetime
    zavod = get_object_or_404(Zavod, zavod_id=pk)
    discipliny_zavodu = DisciplinyZavodu.objects.filter(zavod=zavod).select_related('disciplina')
    vysledky = Vysledek.objects.filter(zavod=zavod).select_related('plavec', 'disciplina')
    
    # Seskupení výsledků podle disciplíny
    vysledky_dict = {}
    for vysledek in vysledky:
        if vysledek.disciplina.nazev not in vysledky_dict:
            vysledky_dict[vysledek.disciplina.nazev] = []
        vysledky_dict[vysledek.disciplina.nazev].append(vysledek)
    
    # Seřazení podle umístění
    for key in vysledky_dict:
        vysledky_dict[key] = sorted(vysledky_dict[key], key=lambda x: x.umisteni)
    
    # Přihlášení plavci (unikátní plavci s výsledky)
    prihlasen_plavci = Plavec.objects.filter(vysledek__zavod=zavod).distinct()
    
    # Zkontroluj zda je závod již proběhnutý
    is_past_event = zavod.datum < datetime.now().date() if zavod.datum else False
    
    context = {
        'zavod': zavod,
        'discipliny_zavodu': discipliny_zavodu,
        'vysledky_dict': vysledky_dict,
        'total_vysledky': vysledky.count(),
        'prihlasen_plavci': prihlasen_plavci,
        'is_past_event': is_past_event,
    }
    return render(request, 'zavody/zavod_detail.html', context)

# Seznam všech plavců
def plavci_list(request):
    plavci = Plavec.objects.all().select_related('klub', 'stat')
    
    # Filtrování
    query = request.GET.get('q')
    klub_filter = request.GET.get('klub')
    pohlavi_filter = request.GET.get('pohlavi')
    
    if query:
        plavci = plavci.filter(Q(jmeno__icontains=query) | Q(prijmeni__icontains=query))
    if klub_filter:
        plavci = plavci.filter(klub_id=klub_filter)
    if pohlavi_filter:
        plavci = plavci.filter(pohlavi=pohlavi_filter)
    
    kluby = Klub.objects.all()
    
    context = {
        'plavci': plavci,
        'kluby': kluby,
        'query': query,
        'klub_filter': klub_filter,
        'pohlavi_filter': pohlavi_filter,
    }
    return render(request, 'zavody/plavci_list.html', context)

# Detail plavce
def plavec_detail(request, pk):
    plavec = get_object_or_404(Plavec, plavec_id=pk)
    vysledky = Vysledek.objects.filter(plavec=plavec).select_related('zavod', 'disciplina')
    treneri = plavec.treneri.all()
    
    context = {
        'plavec': plavec,
        'vysledky': vysledky,
        'treneri': treneri,
    }
    return render(request, 'zavody/plavec_detail.html', context)

# Seznam klubů
def kluby_list(request):
    kluby = Klub.objects.all().select_related('mesto', 'mesto__stat').annotate()
    
    query = request.GET.get('q')
    if query:
        kluby = kluby.filter(Q(nazev__icontains=query) | Q(mesto__nazev__icontains=query))
    
    context = {'kluby': kluby, 'query': query}
    return render(request, 'zavody/kluby_list.html', context)

# Detail klubu
def klub_detail(request, pk):
    klub = get_object_or_404(Klub, klub_id=pk)
    plavci = Plavec.objects.filter(klub=klub)
    treneri = klub.trener_set.all()
    
    context = {
        'klub': klub,
        'plavci': plavci,
        'treneri': treneri,
    }
    return render(request, 'zavody/klub_detail.html', context)

# Seznam zemí
def stat_list(request):
    stavy = Stat.objects.all()
    context = {'stavy': stavy}
    return render(request, 'zavody/stat_list.html', context)

# Detail země
def stat_detail(request, pk):
    stat = get_object_or_404(Stat, stat_id=pk)
    mesta = stat.mesto_set.all()
    plavci = Plavec.objects.filter(stat=stat)
    
    context = {
        'stat': stat,
        'mesta': mesta,
        'plavci': plavci,
    }
    return render(request, 'zavody/stat_detail.html', context)

# Přihlášení
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Vítejte, {user.first_name or user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Nesprávné uživatelské jméno nebo heslo.')
    
    return render(request, 'zavody/login.html')

# Odhlášení
def logout_view(request):
    logout(request)
    messages.success(request, 'Byli jste odhlášeni.')
    return redirect('home')

# Registrace
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        klub_id = request.POST.get('klub') if role == 'trener' else None
        
        if not role:
            messages.error(request, 'Vyberte prosím roli (plavec nebo trenér).')
            return redirect('register')
        
        if role == 'trener' and not klub_id:
            messages.error(request, 'Trenéři musí vybrat klub.')
            return redirect('register')
        
        if password != password2:
            messages.error(request, 'Hesla se neshodují.')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Toto uživatelské jméno již existuje.')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Tento email již existuje.')
            return redirect('register')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Vytvořit UserProfile s rolí
        from .models import UserProfile
        UserProfile.objects.create(user=user, role=role)
        
        # Pokud je trenér, vytvoř Trener záznam s klubem
        if role == 'trener' and klub_id:
            from .models import Trener, Klub, Stat
            try:
                klub = Klub.objects.get(klub_id=klub_id)
                # Zjisti stát z klubu
                stat = klub.mesto.stat if klub.mesto else None
                Trener.objects.get_or_create(
                    jmeno=first_name,
                    prijmeni=last_name,
                    defaults={'klub': klub, 'stat': stat}
                )
            except Klub.DoesNotExist:
                pass
        
        messages.success(request, 'Registrace byla úspěšná! Nyní se prosím přihlaste.')
        return redirect('login')
    
    from .models import Klub
    kluby = Klub.objects.all().order_by('nazev')
    
    return render(request, 'zavody/register.html', {'kluby': kluby})

# Profil přihlášeného uživatele
@login_required(login_url='login')
def profile_view(request):
    context = {
        'user': request.user,
    }
    return render(request, 'zavody/profile.html', context)

# Seznam trenérů
def treneri_list(request):
    treneri = Trener.objects.all().select_related('klub', 'stat')
    
    query = request.GET.get('q')
    klub_filter = request.GET.get('klub')
    
    if query:
        treneri = treneri.filter(Q(jmeno__icontains=query) | Q(prijmeni__icontains=query))
    if klub_filter:
        treneri = treneri.filter(klub_id=klub_filter)
    
    kluby = Klub.objects.all()
    
    context = {
        'treneri': treneri,
        'kluby': kluby,
        'query': query,
        'klub_filter': klub_filter,
    }
    return render(request, 'zavody/treneri_list.html', context)

# Detail trenéra
def trener_detail(request, pk):
    trener = get_object_or_404(Trener, trener_id=pk)
    plavci = trener.plavci.all()
    
    context = {
        'trener': trener,
        'plavci': plavci,
    }
    return render(request, 'zavody/trener_detail.html', context)

# Přidání svěřence trenérem
@login_required(login_url='login')
def add_sverenek(request):
    # Zkontroluj, zda je uživatel trenér
    try:
        # Kontroluj roli přes UserProfile
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'trener':
            messages.error(request, 'Nejste zaregistrován/a jako trenér.')
            return redirect('home')
        
        # Najdi trenéra asociovaného s tímto uživatelem
        treneri = Trener.objects.filter(jmeno__icontains=request.user.first_name) if request.user.first_name else Trener.objects.filter(jmeno__icontains=request.user.username)
        if not treneri.exists():
            # Pokud neexistuje, vytvoř nový Trener záznam
            trener = Trener.objects.create(
                jmeno=request.user.first_name or request.user.username,
                prijmeni=request.user.last_name or '',
                klub_id=1  # Default klub (měl by existovat)
            )
        else:
            trener = treneri.first()
        
        if request.method == 'POST':
            plavec_id = request.POST.get('plavec_id')
            plavec = get_object_or_404(Plavec, plavec_id=plavec_id)
            
            if trener.plavci.filter(plavec_id=plavec_id).exists():
                messages.warning(request, 'Tento plavec je již ve vašem seznamu.')
            else:
                trener.plavci.add(plavec)
                messages.success(request, f'Plavec {plavec.jmeno} {plavec.prijmeni} byl přidán do vašeho seznamu.')
            
            return redirect('add_sverenek')
        
        # Vyber všechny plavce, které trenér nemá
        visi_plavci = Plavec.objects.exclude(treneri__trener_id=trener.trener_id)
        
        context = {
            'trener': trener,
            'visi_plavci': visi_plavci,
            'soucasni_plavci': trener.plavci.all(),
        }
        return render(request, 'zavody/add_sverenek.html', context)
    except Exception as e:
        messages.error(request, 'Došlo k chybě. Kontaktujte administrátora.')
        return redirect('profile')


# Zápis plavců trenéra na závody
@login_required(login_url='login')
def zapsat_plavce_na_zavod(request):
    """Stránka pro zápis vlastních plavců na závody"""
    try:
        # Kontroluj roli přes UserProfile
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'trener':
            messages.error(request, 'Nejste zaregistrován/a jako trenér.')
            return redirect('home')
        
        # Najít trenéra podle user.first_name
        treneri = Trener.objects.filter(jmeno__icontains=request.user.first_name) if request.user.first_name else Trener.objects.filter(jmeno__icontains=request.user.username)
        if not treneri.exists():
            # Pokud neexistuje, vytvoř nový Trener záznam
            trener = Trener.objects.create(
                jmeno=request.user.first_name or request.user.username,
                prijmeni=request.user.last_name or '',
                klub_id=1  # Default klub (měl by existovat)
            )
        else:
            trener = treneri.first()
        
        if request.method == 'POST':
            zavod_id = request.POST.get('zavod_id')
            plavci_ids = request.POST.getlist('plavci')
            discipliny_ids = request.POST.getlist('discipliny')
            
            if not zavod_id:
                messages.error(request, 'Vyberte prosím závod.')
                return redirect('zapsat_plavce_na_zavod')
            
            if not discipliny_ids:
                messages.error(request, 'Vyberte prosím alespoň jednu disciplinu.')
                return redirect('zapsat_plavce_na_zavod')
            
            zavod = get_object_or_404(Zavod, zavod_id=zavod_id)
            
            # Přidat plavce na závod
            if plavci_ids:
                for plavec_id in plavci_ids:
                    try:
                        plavec = get_object_or_404(Plavec, plavec_id=plavec_id)
                        # Zkontrolovat, zda je plavec ve svěřencích trenéra
                        if trener.plavci.filter(plavec_id=plavec_id).exists():
                            # Přidat do závodu - vytvoř Vysledek POUZE pro vybrané discipliny
                            for disciplina_id in discipliny_ids:
                                try:
                                    disciplina = Disciplina.objects.get(disciplina_id=disciplina_id)
                                    # Zkontrolovat, zda už existuje záznam
                                    if not Vysledek.objects.filter(zavod=zavod, plavec=plavec, disciplina=disciplina).exists():
                                        Vysledek.objects.create(
                                            zavod=zavod,
                                            plavec=plavec,
                                            disciplina=disciplina,
                                            umisteni=999  # Default placeholder
                                        )
                                except Disciplina.DoesNotExist:
                                    pass
                            messages.success(request, f'Plavec {plavec.jmeno} {plavec.prijmeni} byl zapsán na {len(discipliny_ids)} disciplin.')
                        else:
                            messages.warning(request, f'{plavec.jmeno} {plavec.prijmeni} není ve vašem seznamu svěřenců.')
                    except Exception as e:
                        messages.error(request, f'Chyba při zápisu plavce: {str(e)}')
                
                messages.info(request, 'Zápis plavců byl zaregistrován.')
            else:
                messages.warning(request, 'Vyberte alespoň jednoho plavce.')
            
            return redirect('zapsat_plavce_na_zavod')
        
        # Všechny budoucí závody
        from datetime import datetime
        budouci_zavody = Zavod.objects.filter(datum__gte=datetime.now().date()).order_by('datum')
        
        # Připrav discipliny pro každý závod
        zavody_with_disciplines = []
        for zavod in budouci_zavody:
            disciplines = DisciplinyZavodu.objects.filter(zavod=zavod).select_related('disciplina').order_by('zacatek')
            zavody_with_disciplines.append({
                'zavod': zavod,
                'disciplines': disciplines
            })
        
        context = {
            'trener': trener,
            'budouci_zavody': budouci_zavody,
            'zavody_with_disciplines': zavody_with_disciplines,
            'soucasni_plavci': trener.plavci.all(),
        }
        return render(request, 'zavody/zapsat_plavce_na_zavod.html', context)
    except Exception as e:
        messages.error(request, 'Došlo k chybě. Kontaktujte administrátora.')
        return redirect('profile')

# Přidání plavce do klubu trenérem
@login_required
def add_plavec_to_klub(request):
    if request.user.profile.role != 'trener':
        messages.error(request, 'Přístup pouze pro trenéry.')
        return redirect('home')
    
    try:
        # Získej trenéra a jeho klub
        trener = Trener.objects.get(
            jmeno=request.user.first_name or '',
            prijmeni=request.user.last_name or ''
        )
        klub = trener.klub
        
        if not klub:
            messages.error(request, 'Trenér nemá přiřazený klub.')
            return redirect('profile')
        
        if request.method == 'POST':
            plavec_id = request.POST.get('plavec_id')
            
            if plavec_id:
                try:
                    plavec = Plavec.objects.get(plavec_id=plavec_id)
                    # Přiřaď plavce do klubu
                    plavec.klub = klub
                    plavec.save()
                    messages.success(request, f'{plavec.jmeno} {plavec.prijmeni} byl/a přidán/a do klubu {klub.nazev}.')
                    return redirect('profile')
                except Plavec.DoesNotExist:
                    messages.error(request, 'Plavec nebyl nalezen.')
            else:
                messages.error(request, 'Vyberte plavce.')
        
        # Zobraz seznam plavců bez klubu nebo s jiným klubem
        plavci_bez_klubu = Plavec.objects.filter(klub__isnull=True)
        plavci_jiny_klub = Plavec.objects.exclude(klub=klub)
        
        context = {
            'klub': klub,
            'trener': trener,
            'plavci_bez_klubu': plavci_bez_klubu,
            'plavci_jiny_klub': plavci_jiny_klub,
        }
        return render(request, 'zavody/add_plavec_to_klub.html', context)
    except Trener.DoesNotExist:
        messages.error(request, 'Trenér nebyl nalezen v systému.')
        return redirect('profile')
    except Exception as e:
        messages.error(request, 'Došlo k chybě.')
        return redirect('profile')
