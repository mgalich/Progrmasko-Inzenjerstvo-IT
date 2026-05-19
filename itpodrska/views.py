from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def korisnik_u_grupi(user, naziv_grupe):
    return user.groups.filter(name=naziv_grupe).exists()

@login_required
def pocetna(request):
    if request.user.groups.filter(name='Zaposlenik').exists():
        return render(request, 'itpodrska/dashboard_zaposlenik.html')

    if request.user.groups.filter(name='IT djelatnik').exists():
        return render(request, 'itpodrska/dashboard_it.html')

    if request.user.groups.filter(name='Voditelj IT odjela').exists():
        return render(request, 'itpodrska/dashboard_voditelj.html')

    if request.user.groups.filter(name='Administrator').exists():
        return render(request, 'itpodrska/dashboard_admin.html')

    return render(request, 'itpodrska/dashboard.html')

from .models import Zahtjev, Incident, ItOprema, ClanakBazeZnanja, Izvjestaj, ItZaposlenik

@login_required
def zahtjevi(request):
    svi_zahtjevi = Zahtjev.objects.all()
    return render(request, 'itpodrska/zahtjevi.html', {'zahtjevi': svi_zahtjevi})

@login_required
def incidenti(request):
    svi_incidenti = Incident.objects.all()
    return render(request, 'itpodrska/incidenti.html', {'incidenti': svi_incidenti})

@login_required
def oprema(request):
    sva_oprema = ItOprema.objects.all()
    return render(request, 'itpodrska/oprema.html', {'oprema': sva_oprema})

@login_required
def baza_znanja(request):
    clanci = ClanakBazeZnanja.objects.all()
    return render(request, 'itpodrska/baza_znanja.html', {'clanci': clanci})

@login_required
def izvjestaji(request):
    svi_izvjestaji = Izvjestaj.objects.all()
    return render(request, 'itpodrska/izvjestaji.html', {'izvjestaji': svi_izvjestaji})

from django.shortcuts import render, redirect
from .models import Zahtjev, Incident, ItOprema,ClanakBazeZnanja, Izvjestaj
from datetime import date

@login_required
def novi_zahtjev(request):

    if request.method == "POST":

        Zahtjev.objects.create(
            naslov_zahtjeva=request.POST["naslov_zahtjeva"],
            opis_zahtjeva=request.POST["opis_zahtjeva"],
            datum_prijave=request.POST["datum_prijave"]
        )

        return redirect('/zahtjevi/')

    return render(request, 'itpodrska/novi_zahtjev.html')

@login_required
def novi_incident(request):
    if request.method == "POST":
        Incident.objects.create(
            naziv_incidenta=request.POST["naziv_incidenta"],
            opis_incidenta=request.POST["opis_incidenta"],
            datum_prijave=request.POST["datum_prijave"],
            lokacija=request.POST["lokacija"]
        )

        return redirect('/incidenti/')

    return render(request, 'itpodrska/novi_incident.html')

@login_required
def nova_oprema(request):
    if request.method == "POST":
        ItOprema.objects.create(
            inventarni_broj=request.POST["inventarni_broj"],
            naziv_opreme=request.POST["naziv_opreme"],
            vrsta_opreme=request.POST["vrsta_opreme"],
            proizvodjac=request.POST["proizvodjac"],
            model=request.POST["model"],
            serijski_broj=request.POST["serijski_broj"],
            lokacija=request.POST["lokacija"],
            datum_kupnje=request.POST["datum_kupnje"] or None,
            jamstvo_mjeseci=request.POST["jamstvo_mjeseci"] or None
        )

        return redirect('/oprema/')

    return render(request, 'itpodrska/nova_oprema.html')

@login_required
def novi_clanak(request):
    if request.method == "POST":
        ClanakBazeZnanja.objects.create(
            naslov_clanka=request.POST["naslov_clanka"],
            opis_problema=request.POST["opis_problema"],
            opis_rjesenja=request.POST["opis_rjesenja"],
            kljucne_rijeci=request.POST["kljucne_rijeci"],
            datum_unosa=request.POST["datum_unosa"]
        )

        return redirect('/baza-znanja/')

    return render(request, 'itpodrska/novi_clanak.html')

def odjava(request):
    logout(request)
    return redirect('/login/')

@login_required
def dodijeli_zahtjeve(request):
    it_djelatnici = ItZaposlenik.objects.all()
    zahtjevi = Zahtjev.objects.all()
    incidenti = Incident.objects.all()

    return render(request, 'itpodrska/dodijeli_zahtjeve.html', {
        'it_djelatnici': it_djelatnici,
        'zahtjevi': zahtjevi,
        'incidenti': incidenti
    })