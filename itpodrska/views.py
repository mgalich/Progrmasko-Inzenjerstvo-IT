from django.shortcuts import render

def pocetna(request):
    return render(request, 'itpodrska/dashboard.html')

from .models import Zahtjev, Incident, ItOprema, ClanakBazeZnanja, Izvjestaj

def zahtjevi(request):
    svi_zahtjevi = Zahtjev.objects.all()
    return render(request, 'itpodrska/zahtjevi.html', {'zahtjevi': svi_zahtjevi})


def incidenti(request):
    svi_incidenti = Incident.objects.all()
    return render(request, 'itpodrska/incidenti.html', {'incidenti': svi_incidenti})

def oprema(request):
    sva_oprema = ItOprema.objects.all()
    return render(request, 'itpodrska/oprema.html', {'oprema': sva_oprema})

def baza_znanja(request):
    clanci = ClanakBazeZnanja.objects.all()
    return render(request, 'itpodrska/baza_znanja.html', {'clanci': clanci})

def izvjestaji(request):
    svi_izvjestaji = Izvjestaj.objects.all()
    return render(request, 'itpodrska/izvjestaji.html', {'izvjestaji': svi_izvjestaji})

