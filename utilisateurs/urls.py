from django.urls import path
from utilisateurs.views import Acceuil,Connexion,Deconnexion,formulaire,forget_password,update_password,confirmation,user_profile,update_profile

urlpatterns =[
    path('', Acceuil,name='Acceuil'),
    path('Connexion', Connexion,name='Connexion'),
    path('Deconnexion', Deconnexion,name='Deconnexion'),
    path('formulaire', formulaire,name='formulaire'),
    path('forget_password', forget_password,name='forget_password'),
    path("update-password/<str:token>/<str:uid>/",update_password,name="update_password" ),
    path('confirmation/<uidb64>/<token>/', confirmation, name='confirmation'),
    path('profile/', user_profile, name='user_profile'),
    path('update_profile/', update_profile, name='update_profile'),

]