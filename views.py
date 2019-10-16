from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Chezsoi, Personnegrc, Municipalite, Liberation
from django.contrib import messages
from .forms import PersonneForm, ChezsoiForm, LiberationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bootstrap_datepicker_plus import DateTimePickerInput
import datetime
#from django.db import connection


## Affiche la liste des dossiers encore ouverts
@login_required(login_url=settings.LOGIN_URI)
def liste_personne(request):
    entete = settings.SITE_HEADER + " : Listing"
    personne_list = Personnegrc.objects.filter(ferme=0)
    paginator = Paginator(personne_list, 100)
    page = request.GET.get('page')
    try:
        personnes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        personnes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        personnes = paginator.page(paginator.num_pages)
    return render(request, 'listechezsoi.html', {'personnes': personnes, 'entete': entete})


## Pour clore les dossiers terminés
@login_required(login_url=settings.LOGIN_URI)
def personne_ferme(request, pk):
    personne = Personnegrc.objects.get(pk=pk)
    personne.ferme =1
    personne.save()
    messages.success(request, "Fermeture de " + personne.codeGRC )
    return redirect('liste_personne')


## Pour vérifier si de nouveaux délits sont présents dans les fiches
@login_required(login_url=settings.LOGIN_URI)
def personne_edit(request, pk):
    personne = Personnegrc.objects.get(pk=pk)
    entete = settings.SITE_HEADER + " : Mise à jour"
    date_old_sentence = datetime.date(1900, 1, 1)
    oldfps = personne.oldpresencefps
    if Chezsoi.objects.filter(personnegrc=personne).exists():
        dernieredate = Chezsoi.objects.filter(personnegrc=personne).order_by('-date_sentence').first()
        date_old_sentence = dernieredate.date_sentence

    if request.method == 'POST':
        form = PersonneForm(request.POST, instance=personne)
        if form.is_valid():
            personne = form.save(commit=False)
            personne.RA = request.user
            # print(request.POST.get('dateprint2').__class__)
            newfps = request.POST.get('newpresencefps')
            date_new_sentence = datetime.date(1900, 1, 1)
            if request.POST.get('dateverdictder') != "":
                jour, mois, an = request.POST.get('dateverdictder').split('/')
                date_new_sentence = datetime.date(int(an), int(mois), int(jour))
            timediff = date_new_sentence - date_old_sentence

            if timediff.days > 1:
                personne.newdelit = 1
                messages.success(request, "La personne a été mise à jour.")
            else:
                personne.newdelit = 0
                personne.ferme = 1
                messages.success(request, "La personne a été mise à jour et le dossier fermé.")
            personne.save()
            if (date_new_sentence > date_old_sentence) | (oldfps == 0 and newfps == 1):
                return redirect('personne_delits', personne.id)
            else:
                return redirect('liste_personne')
        else:
            messages.error(request, "Il y a une erreur dans l'enregistrement")
            return redirect('personne_edit', personne.id)
    else:
        form = PersonneForm(instance=personne)
        form.fields['dateprint2'].widget = DateTimePickerInput(format='%d/%m/%Y')
        form.fields['dateverdictder'].widget = DateTimePickerInput(format='%d/%m/%Y')
    return render(request, "personne_edit.html", {'my_form': form, 'entete': entete, 'personne': personne})


## Permet sur une même page d'enregistrer les délits, les libérations et de voir ce qui est déjà rentré
@login_required(login_url=settings.LOGIN_URI)
def personne_delits(request, pk):
    personne = Personnegrc.objects.get(pk=pk)
    delits = Chezsoi.objects.filter(personnegrc=personne).order_by('-date_sentence')
    liberations = Liberation.objects.filter(personnegrc=personne).order_by('-date_liberation')
    entete = settings.SITE_HEADER + " : Délits "
    # Fait la liste des villes de la province correspondante et ajoute les autres
    ville = Municipalite.objects.filter(Q(province=personne.province) | Q(province=5))
    form = ChezsoiForm(prefix='delit')
    form.fields['lieu_sentence'].queryset = ville
    # form.fields['date_sentence'].widget = DateTimePickerInput(format='%d/%m/%Y')
    libe_form = LiberationForm(prefix='libe')
    # libe_form.fields['date_liberation'].widget = DateTimePickerInput(format='%d/%m/%Y')
    if request.method == 'POST':
        if 'Savelibe' or 'Savelibequit' in request.POST:
            libe_form = LiberationForm(request.POST, prefix='libe')
            form = ChezsoiForm(prefix='delit')
            if libe_form.is_valid():
                libe = libe_form.save(commit=False)
                libe.RA = request.user
                libe.personnegrc = personne
                libe.save()
                messages.success(request, "Une liberation de " + personne.codeGRC + " a été ajoutée.")
                if 'Savelibequit' in request.POST:
                    return redirect('liste_personne')
                elif 'Savelibe':
                    return redirect('personne_delits', personne.id )
        if not libe_form.is_valid():
            if 'Savequit' or 'Savedelit' in request.POST:
                form = ChezsoiForm(request.POST, prefix='delit')
                libe_form = LiberationForm(prefix='libe')
                if form.is_valid():
                    delit = form.save(commit=False)
                    delit.RA = request.user
                    delit.personnegrc = personne
                    delit.province = personne.province
                    delit.nouveaudelit = 1
                    delit.save()
                    messages.success(request, "Les delits du # " + personne.codeGRC + " ont été mis à jour.")
                    if 'Savequit' in request.POST:
                        return redirect('liste_personne')
                    else:
                        return redirect('personne_delits', personne.id)
        if not libe_form.is_valid():
            messages.error(request, "Il y a une erreur dans l'enregistrement de la liberation")
        if not form.is_valid():
            messages.error(request, "Il y a une erreur dans l'enregistrement du delit")
    return render(request, "personne_delits.html", {'personne': personne,
                                                    'delits': delits,
                                                    'liberations': liberations,
                                                    'form': form,
                                                    'libe_form': libe_form,
                                                    'entete' : entete})