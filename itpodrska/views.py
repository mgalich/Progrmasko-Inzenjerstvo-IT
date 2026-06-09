from datetime import date

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    ClanakBazeZnanja,
    Incident,
    ItOprema,
    ItZaposlenik,
    Izvjestaj,
    PrioritetIncidenta,
    PrioritetZahtjeva,
    StatusIncidenta,
    StatusOpreme,
    StatusZahtjeva,
    TipZahtjeva,
    Zahtjev,
    Zaposlenik,
)


def korisnik_u_grupi(user, naziv_grupe):
    return user.groups.filter(name=naziv_grupe).exists()


def _prvi_status(model, polje, nazivi):
    for naziv in nazivi:
        zapis = model.objects.filter(**{f"{polje}__iexact": naziv}).first()
        if zapis:
            return zapis
    return model.objects.first()


def _zaposlenik_za_korisnika(user):
    if not user.is_authenticated:
        return None
    if user.email:
        zaposlenik = Zaposlenik.objects.filter(email__iexact=user.email).first()
        if zaposlenik:
            return zaposlenik
    return Zaposlenik.objects.filter(email__istartswith=user.username).first()


def _it_zaposlenik_za_korisnika(user):
    if not user.is_authenticated:
        return None
    if user.email:
        it_zaposlenik = ItZaposlenik.objects.filter(email__iexact=user.email).first()
        if it_zaposlenik:
            return it_zaposlenik
    return ItZaposlenik.objects.filter(email__istartswith=user.username).first()


@login_required
def pocetna(request):
    if request.user.groups.filter(name='Zaposlenik').exists():
        return render(request, 'itpodrska/dashboard_zaposlenik.html', {
            'broj_zahtjeva': Zahtjev.objects.count(),
            'broj_incidenata': Incident.objects.count(),
            })

    if request.user.groups.filter(name='IT djelatnik').exists():
        return render(request, 'itpodrska/dashboard_it.html', {
        'broj_zahtjeva': Zahtjev.objects.count(),
        'broj_incidenata': Incident.objects.count(),
        'broj_clanaka': ClanakBazeZnanja.objects.count(),
    })

    if request.user.groups.filter(name='Voditelj IT odjela').exists():
        return render(request, 'itpodrska/dashboard_voditelj.html', {
        'broj_zahtjeva': Zahtjev.objects.count(),
        'broj_incidenata': Incident.objects.count(),
        'broj_izvjestaja': Izvjestaj.objects.count(),
    })

    if request.user.groups.filter(name='Administrator').exists():
        return render(request, 'itpodrska/dashboard_admin.html', {
        'broj_zahtjeva': Zahtjev.objects.count(),
        'broj_incidenata': Incident.objects.count(),
        'broj_opreme': ItOprema.objects.count(),
        'broj_clanaka': ClanakBazeZnanja.objects.count(),
    })

    return render(request, 'itpodrska/dashboard_zaposlenik.html', {
    'broj_zahtjeva': Zahtjev.objects.count(),
    'broj_incidenata': Incident.objects.count(),
})


@login_required
def zahtjevi(request):
    svi_zahtjevi = Zahtjev.objects.all()

    if korisnik_u_grupi(request.user, 'Zaposlenik'):
        zaposlenik = _zaposlenik_za_korisnika(request.user)
        if zaposlenik:
            svi_zahtjevi = svi_zahtjevi.filter(id_zaposlenika=zaposlenik)

    if korisnik_u_grupi(request.user, 'IT djelatnik'):
        it_zaposlenik = _it_zaposlenik_za_korisnika(request.user)
        if it_zaposlenik:
            svi_zahtjevi = svi_zahtjevi.filter(id_it_zaposlenika=it_zaposlenik)

    return render(request, 'itpodrska/zahtjevi.html', {'zahtjevi': svi_zahtjevi})


@login_required
def incidenti(request):
    svi_incidenti = Incident.objects.all()

    if korisnik_u_grupi(request.user, 'Zaposlenik'):
        zaposlenik = _zaposlenik_za_korisnika(request.user)
        if zaposlenik:
            svi_incidenti = svi_incidenti.filter(id_zaposlenika=zaposlenik)

    if korisnik_u_grupi(request.user, 'IT djelatnik'):
        it_zaposlenik = _it_zaposlenik_za_korisnika(request.user)
        if it_zaposlenik:
            svi_incidenti = svi_incidenti.filter(id_it_zaposlenika=it_zaposlenik)

    return render(request, 'itpodrska/incidenti.html', {'incidenti': svi_incidenti})


@login_required
def oprema(request):
    sva_oprema = ItOprema.objects.all()
    return render(request, 'itpodrska/oprema.html', {'oprema': sva_oprema})


@login_required
def baza_znanja(request):
    clanci = ClanakBazeZnanja.objects.all()

    moze_dodati_clanak = (
        korisnik_u_grupi(request.user, "IT djelatnik")
        or korisnik_u_grupi(request.user, "Administrator")
    )

    return render(request, 'itpodrska/baza_znanja.html', {
        'clanci': clanci,
        'moze_dodati_clanak': moze_dodati_clanak
    })

@login_required
def izvjestaji(request):
    svi_izvjestaji = Izvjestaj.objects.all()

    ukupno_zahtjeva = Zahtjev.objects.count()
    ukupno_incidenata = Incident.objects.count()
    ukupno_prijava = ukupno_zahtjeva + ukupno_incidenata

    rijeseni_zahtjevi = Zahtjev.objects.filter(
        id_status_zahtjeva__naziv_statusa_zahtjeva__icontains="rije"
    ).count()

    rijeseni_incidenti = Incident.objects.filter(
        id_status_incidenta__naziv_statusa_incidenta__icontains="rije"
    ).count()

    ukupno_rijesenih = rijeseni_zahtjevi + rijeseni_incidenti
    otvorene_prijave = ukupno_prijava - ukupno_rijesenih

    if ukupno_prijava > 0:
        stopa_rjesavanja = round((ukupno_rijesenih / ukupno_prijava) * 100)
    else:
        stopa_rjesavanja = 0

    opterecenje_it_djelatnika = []

    for djelatnik in ItZaposlenik.objects.all():
        broj_zahtjeva = Zahtjev.objects.filter(id_it_zaposlenika=djelatnik).count()
        broj_incidenata = Incident.objects.filter(id_it_zaposlenika=djelatnik).count()
        ukupno = broj_zahtjeva + broj_incidenata

        opterecenje_it_djelatnika.append({
            "ime": djelatnik.ime,
            "prezime": djelatnik.prezime,
            "zahtjevi": broj_zahtjeva,
            "incidenti": broj_incidenata,
            "ukupno": ukupno,
        })

    return render(request, 'itpodrska/izvjestaji.html', {
        'izvjestaji': svi_izvjestaji,
        'ukupno_zahtjeva': ukupno_zahtjeva,
        'ukupno_incidenata': ukupno_incidenata,
        'ukupno_prijava': ukupno_prijava,
        'rijeseni_zahtjevi': rijeseni_zahtjevi,
        'rijeseni_incidenti': rijeseni_incidenti,
        'ukupno_rijesenih': ukupno_rijesenih,
        'otvorene_prijave': otvorene_prijave,
        'stopa_rjesavanja': stopa_rjesavanja,
        'opterecenje_it_djelatnika': opterecenje_it_djelatnika,
    })


@login_required
def generiraj_izvjestaj(request):
    it_djelatnici = ItZaposlenik.objects.all()

    return render(request, 'itpodrska/generiraj_izvjestaj.html', {
        'it_djelatnici': it_djelatnici,
    })

@login_required
def novi_zahtjev(request):
    tipovi = TipZahtjeva.objects.all()
    prioriteti = PrioritetZahtjeva.objects.all()

    if request.method == "POST":
        Zahtjev.objects.create(
            naslov_zahtjeva=request.POST["naslov_zahtjeva"],
            opis_zahtjeva=request.POST["opis_zahtjeva"],
            datum_prijave=request.POST["datum_prijave"],
            id_zaposlenika=_zaposlenik_za_korisnika(request.user),
            id_tip_zahtjeva=TipZahtjeva.objects.filter(pk=request.POST.get("id_tip_zahtjeva")).first(),
            id_prioritet_zahtjeva=PrioritetZahtjeva.objects.filter(pk=request.POST.get("id_prioritet_zahtjeva")).first(),
            id_status_zahtjeva=_prvi_status(StatusZahtjeva, "naziv_statusa_zahtjeva", ["Otvoreno", "Otvoren", "Zaprimljeno"]),
        )

        return redirect('/zahtjevi/')

    return render(request, 'itpodrska/novi_zahtjev.html', {
        'tipovi': tipovi,
        'prioriteti': prioriteti,
        'danas': date.today(),
    })


@login_required
def novi_incident(request):
    prioriteti = PrioritetIncidenta.objects.all()

    if request.method == "POST":
        Incident.objects.create(
            naziv_incidenta=request.POST["naziv_incidenta"],
            opis_incidenta=request.POST["opis_incidenta"],
            datum_prijave=request.POST["datum_prijave"],
            lokacija=request.POST["lokacija"],
            id_zaposlenika=_zaposlenik_za_korisnika(request.user),
            id_prioritet_incidenta=PrioritetIncidenta.objects.filter(pk=request.POST.get("id_prioritet_incidenta")).first(),
            id_status_incidenta=_prvi_status(StatusIncidenta, "naziv_statusa_incidenta", ["Otvoreno", "Otvoren", "Zaprimljeno"]),
        )

        return redirect('/incidenti/')

    return render(request, 'itpodrska/novi_incident.html', {
        'prioriteti': prioriteti,
        'danas': date.today(),
    })

def generiraj_inventarni_broj():
    najveci_broj = 0

    for oprema in ItOprema.objects.all():
        if oprema.inventarni_broj:
            try:
                broj = int(oprema.inventarni_broj.upper().replace("INV-", ""))
                if broj > najveci_broj:
                    najveci_broj = broj
            except ValueError:
                pass

    sljedeci_broj = najveci_broj + 1

    return f"INV-{sljedeci_broj:03d}"

@login_required
def nova_oprema(request):
    if request.method == "POST":
        obavezna_polja = [
            "naziv_opreme",
            "vrsta_opreme",
            "proizvodjac",
            "model",
            "serijski_broj",
            "lokacija",
            "datum_kupnje",
            "jamstvo_mjeseci",
        ]

        for polje in obavezna_polja:
            if not request.POST.get(polje, "").strip():
                return render(request, 'itpodrska/nova_oprema.html', {
                    "sljedeci_inventarni_broj": generiraj_inventarni_broj(),
                    "greska": "Potrebno je ispuniti sva polja prije spremanja opreme."
                })

        ItOprema.objects.create(
            inventarni_broj=generiraj_inventarni_broj(),
            naziv_opreme=request.POST["naziv_opreme"].strip(),
            vrsta_opreme=request.POST["vrsta_opreme"].strip(),
            proizvodjac=request.POST["proizvodjac"].strip(),
            model=request.POST["model"].strip(),
            serijski_broj=request.POST["serijski_broj"].strip(),
            lokacija=request.POST["lokacija"].strip(),
            datum_kupnje=request.POST["datum_kupnje"],
            jamstvo_mjeseci=request.POST["jamstvo_mjeseci"],
            id_status_opreme=_prvi_status(StatusOpreme, "naziv_statusa_opreme", ["Aktivna", "U upotrebi"])
        )

        return redirect('/oprema/')

    return render(request, 'itpodrska/nova_oprema.html', {
        "sljedeci_inventarni_broj": generiraj_inventarni_broj()
    })

@login_required
def obrisi_opremu(request, id_opreme):
    if request.method == "POST":
        oprema = get_object_or_404(ItOprema, id_opreme=id_opreme)
        oprema.delete()

    return redirect('/oprema/')

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
    if request.method == "POST":
        it_zaposlenik = get_object_or_404(ItZaposlenik, pk=request.POST.get("id_it_zaposlenika"))

        if request.POST.get("vrsta") == "zahtjev":
            zahtjev = get_object_or_404(Zahtjev, pk=request.POST.get("id_prijave"))
            zahtjev.id_it_zaposlenika = it_zaposlenik
            zahtjev.save()

        if request.POST.get("vrsta") == "incident":
            incident = get_object_or_404(Incident, pk=request.POST.get("id_prijave"))
            incident.id_it_zaposlenika = it_zaposlenik
            incident.save()

        return redirect('/dodijeli-zahtjeve/')

    it_djelatnici = ItZaposlenik.objects.all()
    zahtjevi = Zahtjev.objects.filter(id_it_zaposlenika__isnull=True)
    incidenti = Incident.objects.filter(id_it_zaposlenika__isnull=True)

    return render(request, 'itpodrska/dodijeli_zahtjeve.html', {
        'it_djelatnici': it_djelatnici,
        'zahtjevi': zahtjevi,
        'incidenti': incidenti
    })
