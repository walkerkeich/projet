from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Ajustez les champs selon vos besoins

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'Biographie', 'photo', 'type_profile']  # Ajustez les champs selon vos besoins
