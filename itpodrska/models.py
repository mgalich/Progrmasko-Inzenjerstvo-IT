# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ClanakBazeZnanja(models.Model):
    id_clanka = models.AutoField(primary_key=True)
    naslov_clanka = models.CharField(max_length=150)
    opis_problema = models.TextField(blank=True, null=True)
    opis_rjesenja = models.TextField(blank=True, null=True)
    kljucne_rijeci = models.CharField(max_length=200, blank=True, null=True)
    datum_unosa = models.DateField()
    datum_zadnje_izmjene = models.DateField(blank=True, null=True)
    id_it_zaposlenika = models.ForeignKey('ItZaposlenik', models.DO_NOTHING, db_column='id_it_zaposlenika', blank=True, null=True)
    id_kategorije = models.ForeignKey('KategorijaClanka', models.DO_NOTHING, db_column='id_kategorije', blank=True, null=True)
    id_statusa_clanka = models.ForeignKey('StatusClanka', models.DO_NOTHING, db_column='id_statusa_clanka', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clanak_baze_znanja'


class Incident(models.Model):
    id_incidenta = models.AutoField(primary_key=True)
    naziv_incidenta = models.CharField(max_length=100)
    opis_incidenta = models.TextField(blank=True, null=True)
    datum_prijave = models.DateField()
    datum_rjesenja = models.DateField(blank=True, null=True)
    lokacija = models.CharField(max_length=100, blank=True, null=True)
    id_zaposlenika = models.ForeignKey('Zaposlenik', models.DO_NOTHING, db_column='id_zaposlenika', blank=True, null=True)
    id_status_incidenta = models.ForeignKey('StatusIncidenta', models.DO_NOTHING, db_column='id_status_incidenta', blank=True, null=True)
    id_prioritet_incidenta = models.ForeignKey('PrioritetIncidenta', models.DO_NOTHING, db_column='id_prioritet_incidenta', blank=True, null=True)
    id_it_zaposlenika = models.ForeignKey('ItZaposlenik', models.DO_NOTHING, db_column='id_it_zaposlenika', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'incident'


class ItOprema(models.Model):
    id_opreme = models.AutoField(primary_key=True)
    inventarni_broj = models.CharField(unique=True, max_length=50)
    naziv_opreme = models.CharField(max_length=100)
    vrsta_opreme = models.CharField(max_length=50, blank=True, null=True)
    proizvodjac = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    serijski_broj = models.CharField(unique=True, max_length=100, blank=True, null=True)
    lokacija = models.CharField(max_length=100, blank=True, null=True)
    datum_kupnje = models.DateField(blank=True, null=True)
    jamstvo_mjeseci = models.IntegerField(blank=True, null=True)
    id_status_opreme = models.ForeignKey('StatusOpreme', models.DO_NOTHING, db_column='id_status_opreme', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'it_oprema'


class ItZaposlenik(models.Model):
    id_it_zaposlenika = models.AutoField(primary_key=True)
    ime = models.CharField(max_length=50)
    prezime = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'it_zaposlenik'


class Izvjestaj(models.Model):
    id_izvjestaja = models.AutoField(primary_key=True)
    naziv_izvjestaja = models.CharField(max_length=150)
    datum_izrade = models.DateField()
    razdoblje_od = models.DateField(blank=True, null=True)
    razdoblje_do = models.DateField(blank=True, null=True)
    broj_zahtjeva = models.IntegerField(blank=True, null=True)
    broj_incidenata = models.IntegerField(blank=True, null=True)
    broj_rijesenih_prijava = models.IntegerField(blank=True, null=True)
    prosjecno_vrijeme_rjesavanja = models.CharField(max_length=50, blank=True, null=True)
    id_it_zaposlenika = models.ForeignKey(ItZaposlenik, models.DO_NOTHING, db_column='id_it_zaposlenika', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'izvjestaj'


class KategorijaClanka(models.Model):
    id_kategorije = models.AutoField(primary_key=True)
    naziv_kategorije = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'kategorija_clanka'


class KpiPokazatelj(models.Model):
    id_kpi = models.AutoField(primary_key=True)
    naziv_kpi = models.CharField(max_length=100)
    opis_kpi = models.TextField(blank=True, null=True)
    vrijednost_kpi = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    datum_izracuna = models.DateField(blank=True, null=True)
    id_izvjestaja = models.ForeignKey(Izvjestaj, models.DO_NOTHING, db_column='id_izvjestaja', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kpi_pokazatelj'


class PrioritetIncidenta(models.Model):
    id_prioritet_incidenta = models.AutoField(primary_key=True)
    naziv_prioriteta = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'prioritet_incidenta'


class PrioritetZahtjeva(models.Model):
    id_prioritet_zahtjeva = models.AutoField(primary_key=True)
    naziv_prioriteta = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'prioritet_zahtjeva'


class RjesenjeIncidenta(models.Model):
    id_rjesenja_incidenta = models.AutoField(primary_key=True)
    opis_rjesenja = models.TextField()
    datum_rjesenja = models.DateField()
    id_incidenta = models.ForeignKey(Incident, models.DO_NOTHING, db_column='id_incidenta', blank=True, null=True)
    id_it_zaposlenika = models.ForeignKey(ItZaposlenik, models.DO_NOTHING, db_column='id_it_zaposlenika', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rjesenje_incidenta'


class RjesenjeZahtjeva(models.Model):
    id_rjesenja = models.AutoField(primary_key=True)
    opis_rjesenja = models.TextField()
    datum_rjesenja = models.DateField()
    id_zahtjeva = models.ForeignKey('Zahtjev', models.DO_NOTHING, db_column='id_zahtjeva', blank=True, null=True)
    id_it_zaposlenika = models.ForeignKey(ItZaposlenik, models.DO_NOTHING, db_column='id_it_zaposlenika', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rjesenje_zahtjeva'


class StatusClanka(models.Model):
    id_statusa_clanka = models.AutoField(primary_key=True)
    naziv_statusa_clanka = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'status_clanka'


class StatusIncidenta(models.Model):
    id_status_incidenta = models.AutoField(primary_key=True)
    naziv_statusa_incidenta = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'status_incidenta'


class StatusOpreme(models.Model):
    id_status_opreme = models.AutoField(primary_key=True)
    naziv_statusa_opreme = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'status_opreme'


class StatusZahtjeva(models.Model):
    id_status_zahtjeva = models.AutoField(primary_key=True)
    naziv_statusa_zahtjeva = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'status_zahtjeva'


class TipZahtjeva(models.Model):
    id_tip_zahtjeva = models.AutoField(primary_key=True)
    naziv_tipa_zahtjeva = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tip_zahtjeva'


class ZaduzenjeOpreme(models.Model):
    id_zaduzenja = models.AutoField(primary_key=True)
    datum_zaduzenja = models.DateField()
    datum_povrata = models.DateField(blank=True, null=True)
    id_opreme = models.ForeignKey(ItOprema, models.DO_NOTHING, db_column='id_opreme', blank=True, null=True)
    id_zaposlenika = models.ForeignKey('Zaposlenik', models.DO_NOTHING, db_column='id_zaposlenika', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zaduzenje_opreme'


class Zahtjev(models.Model):
    id_zahtjeva = models.AutoField(primary_key=True)
    naslov_zahtjeva = models.CharField(max_length=100)
    opis_zahtjeva = models.TextField(blank=True, null=True)
    datum_prijave = models.DateField()
    datum_zatvaranja = models.DateField(blank=True, null=True)
    id_zaposlenika = models.ForeignKey('Zaposlenik', models.DO_NOTHING, db_column='id_zaposlenika', blank=True, null=True)
    id_tip_zahtjeva = models.ForeignKey(TipZahtjeva, models.DO_NOTHING, db_column='id_tip_zahtjeva', blank=True, null=True)
    id_status_zahtjeva = models.ForeignKey(StatusZahtjeva, models.DO_NOTHING, db_column='id_status_zahtjeva', blank=True, null=True)
    id_prioritet_zahtjeva = models.ForeignKey(PrioritetZahtjeva, models.DO_NOTHING, db_column='id_prioritet_zahtjeva', blank=True, null=True)
    id_it_zaposlenika = models.ForeignKey(ItZaposlenik, models.DO_NOTHING, db_column='id_it_zaposlenika', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zahtjev'


class Zaposlenik(models.Model):
    id_zaposlenika = models.AutoField(primary_key=True)
    ime = models.CharField(max_length=50)
    prezime = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    odjel = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zaposlenik'
