from django import forms
from .models import Cours,Message,Exercice



class CourForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ('id_cours', 'nom', 'position', 'presentation_file', 'video', 'pdf', 'quizz')




class ExerciceForm(forms.ModelForm):
    class Meta:
        model = Exercice
        fields = ['titre', 'fichier', 'description','date_limite']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Écrivez votre message...'}),
        }
