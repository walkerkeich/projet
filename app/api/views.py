from rest_framework import viewsets
from ..models import Filiere, Matiere, Cours, Exercice, Devoir, Message, HistoriqueConsultation
from .serializers import FiliereSerializer, MatiereSerializer, CoursSerializer, ExerciceSerializer, DevoirSerializer, MessageSerializer, HistoriqueConsultationSerializer

from rest_framework.permissions import IsAuthenticated

class FiliereViewSet(viewsets.ModelViewSet):
    queryset = Filiere.objects.all()
    serializer_class = FiliereSerializer
    permission_classes = [IsAuthenticated]

class MatiereViewSet(viewsets.ModelViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer

class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all()
    serializer_class = CoursSerializer

class ExerciceViewSet(viewsets.ModelViewSet):
    queryset = Exercice.objects.all()
    serializer_class = ExerciceSerializer

class DevoirViewSet(viewsets.ModelViewSet):
    queryset = Devoir.objects.all()
    serializer_class = DevoirSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class HistoriqueConsultationViewSet(viewsets.ModelViewSet):
    queryset = HistoriqueConsultation.objects.all()
    serializer_class = HistoriqueConsultationSerializer
