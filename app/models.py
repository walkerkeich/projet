from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import os
from datetime import datetime

def imgFile(inst, filename):
    upload_to = 'Image/'
    fileExt = filename.split('.')[-1]
    if inst.nom:  # Change 'Matiere' to 'inst'
        filename = "imgFile/{}.{}".format(inst.nom, fileExt)
        return os.path.join(upload_to, filename)

class Filiere(models.Model):
    nom = models.CharField(max_length=150, default=' ')
    slug = models.SlugField(null=True, blank=True)
    description = models.CharField(max_length=500)
    img = models.ImageField(upload_to=imgFile, blank=True)

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nom)
        super().save(*args, **kwargs)



class Matiere(models.Model):
    id_mat = models.CharField(unique=True, max_length=100)
    nom = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='matieres')
    img = models.ImageField(upload_to=imgFile, blank=True)
    description = models.CharField(max_length=600)



class HistoriqueConsultation(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultations')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    date_consultation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.matiere.nom} - {self.date_consultation}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

def VideoFile(inst, filename):
    upload_to = 'video/'
    fileExt = filename.split('.')[-1]
    liste = ['mkv', 'mp4', 'mp3', 'avi', 'mov', 'wmv', 'flv', 'mpeg', 'webm', 'ogg']
    if fileExt in liste and inst.nom:
        filename = "VideoFile/{}.{}".format(inst.nom, fileExt)
        return os.path.join(upload_to, filename)
    else:
        raise ValueError('Le format de la vidéo est incompatible')

def PresentationFile(inst, filename):
    upload_to = 'presentation/'
    fileExt = filename.split('.')[-1]
    liste = ['ppt', 'pptx']
    
    if fileExt in liste and inst.nom:
        filename = "Presentation/{}.{}".format(inst.nom, fileExt)
        return os.path.join(upload_to, filename)
    else:
        raise ValueError('Le format de la présentation est incompatible')

def PdfFile(inst, filename):
    upload_to = 'pdf/'
    fileExt = filename.split('.')[-1]
    
    if fileExt == 'pdf' and inst.nom:
        filename = "PDFs/{}.{}".format(inst.nom, fileExt)
        return os.path.join(upload_to, filename)
    else:
        raise ValueError('Le fichier n\'est pas un PDF')




class Cours(models.Model):
    id_cours = models.CharField(primary_key=True, unique=True, max_length=100)
    nom = models.CharField(max_length=100)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    prof = models.ForeignKey(User, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='cours')
    position = models.PositiveSmallIntegerField(verbose_name='chapitre n/')
    video = models.FileField(upload_to=VideoFile, null=True, verbose_name='video', blank=True)
    presentation_file = models.FileField(upload_to=PresentationFile, null=True, verbose_name='powerpoint', blank=True)
    pdf = models.FileField(upload_to=PdfFile, null=True, verbose_name='cours en pdf', blank=True)
    slug = models.SlugField(null=True, blank=True)
    quizz = models.URLField(null=True, blank=True, verbose_name='Lien vers le quiz')  # Modifié ici
    

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nom)
        super().save(*args, **kwargs)




class Exercice(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='exercices')
    titre = models.CharField(max_length=100,blank=True)
    fichier = models.FileField(upload_to='exercices/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date_attribue = models.DateTimeField(auto_now_add=True)
    date_limite = models.DateTimeField(null=True, blank=True)  # Ajout de la date limite

    def __str__(self):
        return self.titre
    
    @property
    def deadline_passed(self):
        return datetime.now() > self.date_limite if self.date_limite else False
    




class Devoir(models.Model):
    exercice = models.ForeignKey('Exercice', on_delete=models.CASCADE, related_name='devoirs')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devoirs')
    fichier = models.FileField(upload_to='devoirs/')
    date_depot = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.exercice.titre}"



class Message(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.contenu[:20]}..."  # Affiche les 20 premiers caractères
