# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from .models import Personnegrc, Chezsoi, Liberation


# Formulaire pour mettre à jour les données de base: présence de nouveaux délits:
class PersonneForm(forms.ModelForm):
    class Meta:
        model = Personnegrc
        fields = ('dateprint2', 'dateverdictder', 'newpresencefps')
        exclude = ('codeGRC', 'province', 'delit', 'dateprint1', 'oldpresencefps', 'assistant', 'newdelit')


class FermeForm(forms.ModelForm):
    class Meta:
        model = Personnegrc
        fields = ('ferme',)
        exclude = ('codeGRC', 'province', 'delit', 'dateprint1', 'oldpresencefps', 'assistant', 'newdelit','dateprint2', 'dateverdictder', 'newpresencefps')


# Formulaire pour rentrer les nouveaux délits si nécessaire:
class ChezsoiForm(forms.ModelForm):
    class Meta:
        model = Chezsoi
        amendeON = forms.BooleanField(required=True)
        detentionON = forms.BooleanField(required=True)
        probationON = forms.BooleanField(required=True)
        interdictionON = forms.BooleanField(required=True)
        surcisON = forms.BooleanField(required=True)
        autreON = forms.BooleanField(required=True)
        fields = ('date_sentence','lieu_sentence','type_tribunal','ordre_delit','codeCCdelit','nombre_chefs','violation',
                  'verdict','amendeON','detentionON','probationON','interdictionON','surcisON','autreON','autredetails')
        exclude = ('RA', 'created_at', 'updated_at', 'card', 'province', 'personnegrc','nouveaudelit')


# Formulaire pour rentrer les libérations:
class LiberationForm(forms.ModelForm):
    class Meta:
        model = Liberation
        type = forms.BooleanField(required=True)
        fields = ('date_liberation','type')
        exclude = ('RA', 'created_at', 'updated_at')




