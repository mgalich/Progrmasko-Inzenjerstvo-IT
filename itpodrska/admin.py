from django.contrib import admin
from .models import (
    Zaposlenik, ItZaposlenik, Zahtjev, TipZahtjeva, StatusZahtjeva,
    PrioritetZahtjeva, RjesenjeZahtjeva, Incident, StatusIncidenta,
    PrioritetIncidenta, RjesenjeIncidenta, ItOprema, StatusOpreme,
    ZaduzenjeOpreme, ClanakBazeZnanja, KategorijaClanka,
    StatusClanka, Izvjestaj, KpiPokazatelj
)

admin.site.register(Zaposlenik)
admin.site.register(ItZaposlenik)
admin.site.register(Zahtjev)
admin.site.register(TipZahtjeva)
admin.site.register(StatusZahtjeva)
admin.site.register(PrioritetZahtjeva)
admin.site.register(RjesenjeZahtjeva)
admin.site.register(Incident)
admin.site.register(StatusIncidenta)
admin.site.register(PrioritetIncidenta)
admin.site.register(RjesenjeIncidenta)
admin.site.register(ItOprema)
admin.site.register(StatusOpreme)
admin.site.register(ZaduzenjeOpreme)
admin.site.register(ClanakBazeZnanja)
admin.site.register(KategorijaClanka)
admin.site.register(StatusClanka)
admin.site.register(Izvjestaj)
admin.site.register(KpiPokazatelj)