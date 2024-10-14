from django.db import models
from django.contrib.auth.models import User,AbstractUser
import os

# Create your models here.
#logique de rennomage des nom de images que l'utilisateur qura uploader
def Photo_order(instance,filename):
    upload_to='Image/'
    fileExt=filename.split('.')[-1]
    if instance.user.username:
        filename="Photo_order/{}.{}".format(instance.user.username , fileExt)
        return os.path.join(upload_to,filename)
    

class Profile(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE)
    Biographie = models.CharField(max_length=500,blank=True)
    photo =models.ImageField(upload_to=Photo_order,blank=True)


    student = 'student'
    prof = 'prof'
    admin ='admin'

    type_user =[
        (student,'student'),(prof,'prof'),(admin,'admin')
    ]
    type_profile =models.CharField(max_length=200,choices=type_user,default="student")
    
    #recupere le nom de l'utilisateur
    def __str__(self):
        return self.user.username
    


