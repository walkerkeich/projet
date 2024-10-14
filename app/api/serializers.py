from rest_framework import serializers
from ..models import Filiere, Matiere, Cours, Exercice, Devoir, Message, HistoriqueConsultation

class FiliereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filiere
        fields = '__all__'

class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = '__all__'

class CoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cours
        fields = '__all__'

class ExerciceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercice
        fields = '__all__'

class DevoirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devoir
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class HistoriqueConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueConsultation
        fields = '__all__'
