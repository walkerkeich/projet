from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect
from.models import *
from django.views.generic import DeleteView,ListView,DeleteView,UpdateView,CreateView,DetailView,RedirectView,View
from .views import *
from .form import CourForm, MessageForm,ExerciceForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import Group

class ProfRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # Vérifier si l'utilisateur appartient au groupe "Prof"
        return self.request.user.groups.filter(name="prof").exists()

from .models import HistoriqueConsultation


def tableau_de_bord(request):
    # Vérifiez si l'utilisateur est connecté
    if request.user.is_authenticated:
        # Récupérer les matières récemment consultées par l'utilisateur
        consultations = HistoriqueConsultation.objects.filter(utilisateur=request.user).order_by('-date_consultation')
        matieres = [consultation.matiere for consultation in consultations]
    else:
        matieres = []

    return render(request, 'programmes/tableau_de_bord.html', {'matieres': matieres})


# Create your views here.

class ListFiliere(ListView):
    context_object_name = 'filieres'
    model=Filiere
    template_name='programmes/Filieres.html'



class ListMatiere(ListView):
    context_object_name = 'matieres'
    model = Filiere
    template_name = 'programmes/matiere.html'

    def get_queryset(self):
        self.filiere = get_object_or_404(Filiere, slug=self.kwargs['slug'])
        matieres = Matiere.objects.filter(filiere=self.filiere)
        return matieres

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filiere'] = self.filiere
        return context



class ListCours(ListView):
    model = Cours
    context_object_name = 'cours'  # Contexte utilisé dans le template
    template_name = 'programmes/Cours.html'

    def get_queryset(self):
        # Récupérer la matière à partir du slug
        self.matiere = get_object_or_404(Matiere, slug=self.kwargs['slug'])
        
        # Enregistrer la consultation
        HistoriqueConsultation.objects.get_or_create(
            utilisateur=self.request.user,
            matiere=self.matiere
        )

        # Retourner les cours liés à cette matière
        return Cours.objects.filter(matiere=self.matiere)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajouter la matière au contexte pour l'utiliser dans le template
        context['matiere'] = self.matiere
        context['filiere'] = self.matiere.filiere 
        return context





class DetailCours(DetailView):
    model = Cours
    template_name = 'programmes/detail_cours.html'
    context_object_name = 'cours'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self):
        slug = self.kwargs['slug']
        return get_object_or_404(Cours, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cours = self.get_object()
        context['video'] = cours.video
        context['presentation'] = cours.presentation_file
        context['pdf'] = cours.pdf
        context['quizz'] = cours.quizz
        context['exercices'] = cours.exercices.all()  # Récupérer tous les exercices associés
        return context


    def post(self, request, *args, **kwargs):
        # Obtenir l'objet courant, généralement l'exercice ou le cours
        self.object = self.get_object()

        # Vérification de la présence du fichier et de l'ID de l'exercice dans la requête
        if 'devoir' in request.FILES and 'exercice_id' in request.POST:
            fichier = request.FILES['devoir']
            exercice_id = request.POST['exercice_id']

            # Récupérer l'exercice correspondant à l'exercice_id
            exercice = get_object_or_404(Exercice, id=exercice_id)

            # Sauvegarder le fichier du devoir dans le modèle Devoir
            Devoir.objects.create(exercice=exercice, fichier=fichier, utilisateur=request.user)

            # Ajouter un message de succès pour confirmer le dépôt
            messages.success(request, 'Votre travail a été déposé avec succès.')

            # Rediriger l'utilisateur vers la page de détails du cours avec un message de succès
            return HttpResponseRedirect(reverse('app:detail_cours', kwargs={'slug': self.object.slug}))

        # Si aucune soumission n'est faite, rediriger vers la même vue
        return self.get(request, *args, **kwargs)# Dans le cas contraire, rechargez la page


class CreerCours(ProfRequiredMixin,CreateView):
    form_class = CourForm
    model = Cours
    template_name = 'programmes/CreerCours.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        matiere_slug = self.kwargs['matiere_slug']
        filiere_slug = self.kwargs['filiere_slug']
        matiere = get_object_or_404(Matiere, slug=matiere_slug, filiere__slug=filiere_slug)
        context['matiere'] = matiere
        context['filiere_slug'] = filiere_slug
        context['exercice_form'] = ExerciceForm()  # Ajout du formulaire d'exercice
        return context

    def form_valid(self, form):
        matiere_slug = self.kwargs['matiere_slug']
        filiere_slug = self.kwargs['filiere_slug']
        matiere = get_object_or_404(Matiere, slug=matiere_slug, filiere__slug=filiere_slug)
        filiere = matiere.filiere
        prof = self.request.user

        # Créer le cours
        form.instance.matiere = matiere
        form.instance.filiere = filiere
        form.instance.prof = prof

        # Sauvegarder le cours dans la base de données
        response = super().form_valid(form)

        # Gestion des exercices
        exercice_form = ExerciceForm(self.request.POST, self.request.FILES)
        if exercice_form.is_valid():
            exercice = exercice_form.save(commit=False)
            exercice.cours = self.object
            exercice.save()
            
        return response

    def get_success_url(self):
        return reverse_lazy('app:cours', kwargs={'category': self.object.filiere.slug, 'slug': self.object.matiere.slug})

def modifier_devoir(request, devoir_id):
    devoir = get_object_or_404(Devoir, id=devoir_id, utilisateur=request.user)
    exercice = devoir.exercice

    # Vérifier si la deadline n'est pas passée
    if exercice.deadline_passed:
        messages.error(request, "La date limite est passée, vous ne pouvez plus modifier votre devoir.")
        return redirect('app:liste_devoirs', exercice_id=exercice.id)

    if request.method == 'POST' and 'nouveau_devoir' in request.FILES:
        nouveau_fichier = request.FILES['nouveau_devoir']
        devoir.fichier = nouveau_fichier
        devoir.save()
        messages.success(request, 'Votre devoir a été modifié avec succès.')
        return redirect('app:liste_devoirs', exercice_id=exercice.id)

    messages.error(request, "Erreur lors de la modification du devoir.")
    return redirect('app:liste_devoirs', exercice_id=exercice.id)



def supprimer_devoir(request, devoir_id):
    devoir = get_object_or_404(Devoir, id=devoir_id, utilisateur=request.user)

    # Supprimer le devoir
    devoir.delete()
    messages.success(request, 'Votre devoir a été supprimé avec succès.')
    
    # Rediriger vers la page de l'exercice ou cours
    return redirect('app:liste_devoirs', exercice_id=devoir.exercice.id)

class ListeDevoirs(View):
    template_name = 'programmes/liste_devoirs.html'

    def get(self, request, exercice_id):
        exercice = get_object_or_404(Exercice, id=exercice_id)
        devoirs = exercice.devoirs.all()  # Récupère tous les devoirs liés à cet exercice
        return render(request, self.template_name, {'exercice': exercice, 'devoirs': devoirs})


class ModifierCours(ProfRequiredMixin,UpdateView):
    model = Cours
    form_class = CourForm
    template_name = 'programmes/ModifierCours.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cours = get_object_or_404(Cours, slug=self.kwargs['slug'])
        context['cours'] = cours
        return context

    def get_success_url(self):
        return reverse_lazy('app:detail_cours', kwargs={'slug': self.object.slug})

class AnnulerModification(ProfRequiredMixin,RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        # Obtenez le cours en utilisant le slug
        cours = get_object_or_404(Cours, slug=self.kwargs['slug'])
        # Redirigez vers la liste des cours de la matière
        return reverse_lazy('app:cours', kwargs={'category': cours.filiere.slug, 'slug': cours.matiere.slug})


class ConfirmationSuppressionCours(ProfRequiredMixin,DeleteView):
    model = Cours
    template_name = 'programmes/SupprimerCours.html'
    
    def get_success_url(self):
        # Redirige vers la liste des cours après suppression
        return reverse_lazy('app:cours', kwargs={'category': self.object.filiere.slug, 'slug': self.object.matiere.slug})
    

def search(request):
    query = request.GET.get('q')  # Récupère la requête de recherche

    if query:
        # Recherche dans les modèles Cours, Matiere et Filiere
        cours = Cours.objects.filter(nom__icontains=query)
        matiere = Matiere.objects.filter(nom__icontains=query)
        filiere = Filiere.objects.filter(nom__icontains=query)
    else:
        cours = Cours.objects.none()
        matiere = Matiere.objects.none()
        filiere = Filiere.objects.none()

    # Context contenant les résultats de la recherche
    context = {
        'cours': cours,
        'matiere': matiere,
        'filiere': filiere,
        'query': query,
    }

    return render(request, 'utilisateurs/search_results.html', context)







@login_required(login_url='Connexion') 
def forum_cours(request, cours_slug):
    cours = get_object_or_404(Cours, slug=cours_slug)
    messages = cours.messages.all()  # Récupère tous les messages pour ce cours

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user  # Assigne l'utilisateur connecté au message
            message.cours = cours
            message.save()
            return redirect('app:forum_cours', cours_slug=cours_slug)
    else:
        form = MessageForm()

    return render(request, 'forum_cours.html', {
        'cours': cours,
        'messages': messages,
        'form': form,
    })