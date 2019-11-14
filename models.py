from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


## Liste des valeurs des choix de
# Code de violation
class Violation(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    def __str__(self):
        return '%s %s' % (self.reponse_valeur, self.reponse_en)


## Tribunaux
class Tribunal(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    def __str__(self):
        return '%s' % self.reponse_en


# Verdicts
class Verdict(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    def __str__(self):
        return '%s' % self.reponse_en


# Provinces
class Province(models.Model):
    reponse_en = models.CharField(max_length=30,)
    reponse_fr = models.CharField(max_length=30,)

    def __str__(self):
        return '%s' % self.reponse_en


# Municipalites par provinces
class Municipalite(models.Model):
    reponse_valeur = models.CharField(max_length=20)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['reponse_en']

    def __str__(self):
        return '%s' % self.reponse_en


## Entrée des données
# Liste de tous les dossiers avec ou sans FPS
class Personnegrc(models.Model):
    codeGRC = models.CharField(max_length=30)
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING)
    delit = models.IntegerField(default=1, verbose_name=_("Présence ancien délits"),)
    alias = models.IntegerField(default=1, verbose_name=_("Présence ancien alias"),)
    dateprint1 = models.DateField(verbose_name=_("Ancienne date print"),)
    oldpresencefps = models.IntegerField(verbose_name=_("Présence ancien FPS"),)
    dateprint2 = models.DateField(verbose_name=_("Date print. Laisser vide si pas de fichier (jj/mm/aaaa)"), blank=True, null=True)
    newdelit = models.BooleanField(default=1, verbose_name=_("Présence de délits après la date du dernier verdict rentré"),)
    newpresencefps = models.BooleanField(verbose_name=_("Présence de FPS en 2019/20. Cocher si oui"))
    dateverdictder = models.DateField(verbose_name=_("Date du dernier verdict présent dans la fiche. Laisser vide si pas de fichier (jj/mm/aaaa)"), blank=True, null=True)
    ferme = models.BooleanField()
    datedeces = models.DateField(verbose_name=_("Si décédé indiquer la date ici (jj/mm/aaaa)"), blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    RA = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['codeGRC']

    def __str__(self):
        return '%s' % self.codeGRC


# Une fiche pour chaque délit de chaque personne.
class Chezsoi(models.Model):
    personnegrc = models.ForeignKey(Personnegrc, on_delete=models.CASCADE)
    date_sentence = models.DateField(verbose_name=_("Date (jj/mm/aaaa)"))
    type_tribunal = models.ForeignKey(Tribunal, on_delete=models.DO_NOTHING, verbose_name="Type de tribunal")
    lieu_sentence = models.ForeignKey(Municipalite, on_delete=models.DO_NOTHING, verbose_name="Lieu du verdict")
    ordre_delit = models.IntegerField(default=1, verbose_name=_("Ordre"),)
    codeCCdelit = models.CharField(max_length=30, verbose_name="Code CC du delit (si pas CC preciser de quel code il s agit)")
    nombre_chefs = models.IntegerField(default=1,)
    violation = models.ForeignKey(Violation, on_delete=models.DO_NOTHING, verbose_name="Code de violation")
    verdict = models.ForeignKey(Verdict, related_name='verdict', on_delete=models.DO_NOTHING)
    amendeON = models.BooleanField(verbose_name="Amende? Cocher si oui")
    detentionON = models.BooleanField(verbose_name="Détention? Cocher si oui")
    probationON = models.BooleanField(verbose_name="Probation? Cocher si oui")
    interdictionON = models.BooleanField(verbose_name="Interdiction? Cocher si oui")
    surcisON = models.BooleanField(verbose_name="Surcis? Cocher si oui")
    autreON = models.BooleanField(verbose_name="Autre? Cocher si oui")
    autredetails = models.CharField(max_length=100, blank=True, null=True,verbose_name="Si autre: détails")
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING)
    old_RA = models.IntegerField(default=1,)
    RA = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    card = models.IntegerField(default=1)
    nouveaudelit = models.BooleanField()

    class Meta:
        ordering = ['personnegrc', 'date_sentence', 'ordre_delit']
        unique_together = (('personnegrc', 'date_sentence', 'ordre_delit','RA'),)
        indexes = [models.Index(fields=['personnegrc', 'date_sentence', 'ordre_delit','RA'])]

    def __str__(self):
        return '%s %s %s' % (self.personnegrc, self.date_sentence, self.ordre_delit)


# Une fiche pour chaque liberation de chaque personne.
class Liberation(models.Model):
    personnegrc = models.ForeignKey(Personnegrc, on_delete=models.CASCADE)
    date_liberation = models.DateField(verbose_name=_("Date de la libération (jj/mm/aaaa)"))
    type = models.BooleanField(verbose_name=_("Libération absolue? Cocher si oui"))
    RA = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['personnegrc', 'date_liberation']

    def __str__(self):
        return '%s %s' % (self.personnegrc, self.date_liberation)