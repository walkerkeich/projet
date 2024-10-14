from django.shortcuts import render,redirect
from .forms import UserForm,ProfilForm
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseForbidden
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.crypto import get_random_string
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import codecs
from django.shortcuts import get_object_or_404
from .models import Profile


def Acceuil(request):
    try:
        return render(request, 'utilisateurs/Acceuil.html')
    except Exception as e:
        print(f"Erreur : {e}")  # Affiche l'erreur dans la console
        return HttpResponse("Erreur dans le chargement du template.")

def user_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'utilisateurs/user_profile.html', {'profile': profile})


@login_required
def update_profile(request):
    profile = request.user.profile  # Suppose que l'utilisateur a un profil associé
    if request.method == 'POST':
        form = ProfilForm(request.POST, request.FILES, instance=profile)  # Récupère les fichiers uploadés
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès.')
            return redirect('update_profile')  # Redirige vers une page de profil ou autre
    else:
        form = ProfilForm(instance=profile)  # Pré-remplit le formulaire avec les données existantes
    
    context = {
        'form2': form,
        'inscrit': True,
    }
    return render(request, 'utilisateurs/update_profile.html', context)

def confirmation(request, uidb64, token):
    try:
        # Décoder l'UID
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, id=uid)

        # Vérifier si le token est valide
        if default_token_generator.check_token(user, token):
            user.is_active = True  # Activer l'utilisateur
            user.save()
            return redirect('Connexion')  # Rediriger vers la page de connexion
        else:
            return render(request, 'utilisateurs/confirmation_invalid.html')  # Token invalide
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return render(request, 'utilisateurs/confirmation_invalid.html')  # Erreur de confirmation



def formulaire(request):
    inscrit = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profil_form = ProfilForm(data=request.POST)
        
        if user_form.is_valid() and profil_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False  # L'utilisateur doit confirmer son e-mail avant d'être actif
            user.save()
            
            profil = profil_form.save(commit=False)
            profil.user = user
            profil.save()

            # Générer un token de confirmation
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)  # Utiliser le générateur de token par défaut

            # Envoyer l'e-mail de confirmation
            current_site = request.META["HTTP_HOST"]
            context = {
                "token": token,
                "uid": uid,
                "domaine": f"http://{current_site}"
            }
            html_text = render_to_string('utilisateurs/email_confirmation.html', context)
            msg = EmailMessage(
                "Confirmez votre inscription",
                html_text,
                "Elearning <tarnaguedac@gmail.com>",
                [user.email],
            )
            msg.content_subtype = 'html'
            msg.send()
            print(f"Email de confirmation envoyé à {user.email}")

            inscrit = True
            return render(request, 'utilisateurs/confirmation_sent.html')  # Afficher un message à l'utilisateur
        else:
            print(user_form.errors, profil_form.errors)
    else:
        user_form = UserForm()
        profil_form = ProfilForm()

    content = {
        'inscrit': inscrit,
        'form1': user_form,
        'form2': profil_form,
    }
    return render(request, 'utilisateurs/formulaire.html', content)


def Connexion(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authentification de l'utilisateur
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                # Connexion réussie
                login(request, user)
                return redirect('/')  # Redirige vers la page d'accueil après connexion
            else:
                return HttpResponse("L'utilisateur est désactivé.")
        else:
            # Si la connexion échoue
            return HttpResponse('Nom d\'utilisateur ou mot de passe incorrect')
    else:
        # Affiche le formulaire de connexion
        return render(request, 'utilisateurs/Connexion.html')
    
@login_required
def Deconnexion (request):
    logout(request)
    return HttpResponseRedirect('/')

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            print('envois')
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            current_site = request.META["HTTP_HOST"]
            context = {"token": token, "uid": uid, "domaine": f"http://{current_site}"}
            html_text=render_to_string('utilisateurs/email.html',context)
            msg = EmailMessage(
                "Réinitialisation de votre mot de passe",
                html_text,
                "Elearning <tarnaguedac@gmail.com>",
                [user.email],
            )
            msg.content_subtype='html'
            msg.send()
            print(f"Email envoyé à {user.email}")
        else:
            print("L'utilisateur n'existe pas.")

    return render(request, 'utilisateurs/forget_password.html', {})


def update_password(request, token, uid):
    try:
        user_id = urlsafe_base64_decode(uid)
        decode_uid = codecs.decode(user_id, "utf-8")
        user = User.objects.get(id=decode_uid)
    except:
        return HttpResponseForbidden(
            "Vous n'aviez pas la permission de modifier ce mot de pass. Utilisateur introuvable"
        )

    check_token = default_token_generator.check_token(user, token)
    if not check_token:
        return HttpResponseForbidden(
            "Vous n'aviez pas la permission de modifier ce mot de pass. Votre Token est invalid ou a espiré"
        )

    error = False
    success = False
    message = ""
    if request.method == "POST":
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")
        print(password, repassword)
        if repassword == password:
            try:
                validate_password(password, user)
                user.set_password(password)
                user.save()

                success = True
                message = "votre mot de pass a été modifié avec succès!"
            except ValidationError as e:
                error = True
                message = str(e)
        else:
            error = True
            message = "Les deux mot de pass ne correspondent pas"

    context = {"error": error, "success": success, "message": message}

    return render(request, "utilisateurs/update_password.html", context)



# Create your views here.
