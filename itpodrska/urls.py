from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.pocetna, name='pocetna'),
    path('zahtjevi/', views.zahtjevi, name='zahtjevi'),
    path('incidenti/', views.incidenti, name='incidenti'),
    path('oprema/', views.oprema, name='oprema'),
    path('baza-znanja/', views.baza_znanja, name='baza_znanja'),
    path('izvjestaji/', views.izvjestaji, name='izvjestaji'),
    path('novi-zahtjev/', views.novi_zahtjev, name='novi_zahtjev'),
    path('novi-incident/', views.novi_incident, name='novi_incident'),
    path('nova-oprema/', views.nova_oprema, name='nova_oprema'),
    path('novi-clanak/', views.novi_clanak, name='novi_clanak' ),
    path('dodijeli-zahtjeve/', views.dodijeli_zahtjeve, name='dodijeli_zahtjeve'),
    path('login/', auth_views.LoginView.as_view(template_name='itpodrska/login.html'), name='login'),
    path('logout/', views.odjava, name='logout'),
    
]