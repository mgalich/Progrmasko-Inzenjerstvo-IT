from django.urls import path
from . import views

urlpatterns = [
    path('', views.pocetna, name='pocetna'),
    path('zahtjevi/', views.zahtjevi, name='zahtjevi'),
    path('incidenti/', views.incidenti, name='incidenti'),
    path('oprema/', views.oprema, name='oprema'),
    path('baza-znanja/', views.baza_znanja, name='baza_znanja'),
    path('izvjestaji/', views.izvjestaji, name='izvjestaji'),
]