from django.conf.urls import url
from django.urls import include, path
from .views import liste_personne, personne_edit, personne_delits, personne_ferme


urlpatterns = [
#    url(r'^code/(?P<pk>[-\w]+)/$', faitinstitution, name='Faitinstitution'),
#    url(r'^code/(?P<pk>[-\w]+)/(?P<choix>[\w]*)/$', faitinstitution, name='Faitinstitution'),
#    url(r'^code/(?P<pk>[-\w]+)/(?P<choix>[\w]*)/(?P<histoire>[\w]*)/$', faitinstitution, name='Faitinstitution'),
    path('personne/<int:pk>/edit/', personne_edit, name='personne_edit'),
    path('delits/<int:pk>/', personne_delits, name='personne_delits'),
    path('', liste_personne, name='liste_personne'),
    path('ferme/<int:pk>/',personne_ferme, name='personne_ferme')
]