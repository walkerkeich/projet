from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Entrez une adresse email valide.")
    class Meta():
        model = User
        fields =[
            
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

        def save(self, commit=True):
            user = super(UserForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user

class ProfilForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields=[
            "Biographie",
            "photo",
            "type_profile"
        ]