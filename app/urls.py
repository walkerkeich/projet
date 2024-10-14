from django.urls import path,include
from app.views import *
app_name='app'

urlpatterns = [
    # Page d'accueil listant les filières
    path('', ListFiliere.as_view(), name='Filieres'),

    # Cours-related paths
    path('cours/<slug:slug>/', DetailCours.as_view(), name='detail_cours'),
    path('cours/<slug:slug>/modifier/', ModifierCours.as_view(), name='modifier_cours'),
    path('cours/<slug:slug>/supprimer/', ConfirmationSuppressionCours.as_view(), name='SupprimerCours'),
    path('cours/<slug:slug>/annuler/', AnnulerModification.as_view(), name='annuler_modification'),
    path('cours/<slug:cours_slug>/forum/', forum_cours, name='forum_cours'),

    # Créer un cours (lié à filière et matière)
    path('creer-cours/<slug:filiere_slug>/<slug:matiere_slug>/', CreerCours.as_view(), name='CreerCours'),

    # Exercice et devoirs
    path('exercice/<int:exercice_id>/devoirs/', ListeDevoirs.as_view(), name='liste_devoirs'),
    path('devoirs/modifier/<int:devoir_id>/', modifier_devoir, name='modifier_devoir'),
    path('devoirs/supprimer/<int:devoir_id>/', supprimer_devoir, name='supprimer_devoir'),

    # Fonctionnalité de recherche
    path('search/', search, name='search'),

    # Tableau de bord
    path('tableau_de_bord/', tableau_de_bord, name='tableau_de_bord'),

    # Listes des cours d'une filière ou matière
    path('<str:category>/<slug:slug>/', ListCours.as_view(), name='cours'),
    path('<slug:slug>/', ListMatiere.as_view(), name='matiere'),

]




