from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FiliereViewSet, MatiereViewSet, CoursViewSet, ExerciceViewSet, DevoirViewSet, MessageViewSet, HistoriqueConsultationViewSet  # Assurez-vous que les imports sont corrects
from rest_framework.authtoken.views import obtain_auth_token
router = DefaultRouter()
router.register(r'filieres', FiliereViewSet)
router.register(r'matieres', MatiereViewSet)
router.register(r'cours', CoursViewSet)
router.register(r'exercices', ExerciceViewSet)
router.register(r'devoirs', DevoirViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'historiques', HistoriqueConsultationViewSet)

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('', include(router.urls)),
]
