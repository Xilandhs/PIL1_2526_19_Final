from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse  # Ajoutez cet import
import json  # Ajoutez cet import
from .models import Users, Profil
from apps.matching.models import Matching, Feedback, Competence
from apps.messaging.models import Messages
from apps.core.models import Matiere
from django.views.decorators.csrf import csrf_exempt

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)
            
            messages.success(request, f'Bienvenue {user.prenom} {user.nom}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Email ou mot de passe incorrect')
            return redirect('login')
    
    return render(request, 'pages/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté')
    return redirect('home')


def register_view(request):
    """Affiche la page d'inscription avec le formulaire à deux étapes"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'pages/register.html')

@csrf_exempt
def register_api_view(request):
    """API pour l'inscription en deux étapes avec points forts/faibles"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Vérifier si l'email existe déjà
        if Users.objects.filter(email=data['email']).exists():
            return JsonResponse({
                'success': False,
                'error': 'Cet email est déjà utilisé'
            }, status=400)
        
        # Vérifier si le matricule existe déjà
        if data.get('matricule') and Users.objects.filter(matricule=data['matricule']).exists():
            return JsonResponse({
                'success': False,
                'error': 'Ce matricule est déjà utilisé'
            }, status=400)
        
        # Créer l'utilisateur
        user = Users.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
            prenom=data['firstName'],
            nom=data['lastName'],
            matricule=data.get('matricule', ''),
            telephone=data.get('phone', ''),
            sexe='M',  # Valeur par défaut, à modifier si vous ajoutez le sexe
            is_active=True
        )
        
        # Créer le profil associé
        profil = Profil.objects.create(
            user=user,
            filiere=data['major'],
            niveau=data['level'],
            format_prefere='les_deux'
        )
        
        # Mapping des sujets vers les matières
        subject_mapping = {
            'maths': 'Mathématiques',
            'coding': 'Programmation',
            'physics': 'Physique',
            'algo': 'Algorithmes',
            'english': 'Anglais',
            'databases': 'Bases de données',
            'economics': 'Économie',
            'stats': 'Statistiques',
            'sysdesign': 'Architecture logicielle',
            'reseaux': 'Réseaux',
            'cybersec': 'Cybersécurité',
        }
        
        # Ajouter les points forts (compétences)
        for subject in data.get('strengths', []):
            matiere_nom = subject_mapping.get(subject, subject)
            matiere, created = Matiere.objects.get_or_create(nom=matiere_nom)
            Competence.objects.create(
                user=user,
                matiere=matiere,
                type='competence'
            )
        
        # Ajouter les points faibles (lacunes)
        for subject in data.get('weaknesses', []):
            matiere_nom = subject_mapping.get(subject, subject)
            matiere, created = Matiere.objects.get_or_create(nom=matiere_nom)
            Competence.objects.create(
                user=user,
                matiere=matiere,
                type='lacune'
            )
        
        # Connecter l'utilisateur
        login(request, user)
        
        return JsonResponse({
            'success': True,
            'redirect_url': '/dashboard/'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Données invalides'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
def profile_view(request):
    """Mon propre profil"""
    user = request.user
    
    competences = Competence.objects.filter(user=user, type='competence').select_related('matiere')
    
    context = {
        'profile_user': user,
        'user': user,
        'competences': competences,
        'is_owner': True,
    }
    return render(request, 'pages/profile.html', context)


@login_required
def user_profile_view(request, user_id):
    """Profil d'un autre utilisateur"""
    profile_user = get_object_or_404(Users, id=user_id)
    
    competences = Competence.objects.filter(user=profile_user, type='competence').select_related('matiere')
    
    context = {
        'profile_user': profile_user,
        'user': profile_user,
        'competences': competences,
        'is_owner': False,
    }
    return render(request, 'pages/profile.html', context)


@login_required
def dashboard_view(request):
    user = request.user
    
    total_sessions = Matching.objects.filter(Q(mentor=user) | Q(mentore=user)).count()
    
    sessions_this_week = Matching.objects.filter(
        Q(mentor=user) | Q(mentore=user),
        created_at__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    total_hours_data = Matching.objects.filter(
        Q(mentor=user) | Q(mentore=user),
        statut='termine'
    ).aggregate(total=Sum('duree_minutes'))
    total_hours = total_hours_data['total'] or 0
    total_hours = total_hours / 60
    
    completed_sessions = Matching.objects.filter(
        Q(mentor=user) | Q(mentore=user),
        statut='termine'
    ).count()
    success_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
    
    avg_rating_data = Feedback.objects.filter(matching__mentor=user).aggregate(avg=Avg('note'))
    avg_rating = avg_rating_data['avg'] or 0
    
    next_session = Matching.objects.filter(
        Q(mentor=user) | Q(mentore=user),
        statut='accepte',
        session_date__gte=timezone.now()
    ).order_by('session_date').first()
    
    upcoming_sessions = Matching.objects.filter(
        Q(mentor=user) | Q(mentore=user),
        statut='accepte',
        session_date__gte=timezone.now()
    ).order_by('session_date')[:3]
    
    unread_messages = Messages.objects.filter(destinataire=user, lu=False).count()
    
    recent_messages = Messages.objects.filter(
        Q(expediteur=user) | Q(destinataire=user)
    ).order_by('-created_at')[:5]
    
    avg_hours_per_session = round(total_hours / total_sessions, 1) if total_sessions > 0 else 0
    
    context = {
        'user': user,
        'total_sessions': total_sessions,
        'sessions_this_week': sessions_this_week,
        'total_hours': round(total_hours, 1),
        'success_rate': round(success_rate),
        'avg_rating': round(avg_rating, 1),
        'avg_hours_per_session': avg_hours_per_session,
        'completed_sessions': completed_sessions,
        'next_session': next_session,
        'upcoming_sessions': upcoming_sessions,
        'unread_messages': unread_messages,
        'recent_messages': recent_messages,
    }
    
    return render(request, 'pages/dashboard.html', context)


@login_required
def edit_profile_view(request):
    user = request.user
    
    # Récupérer ou créer le profil
    try:
        profil = user.profil
    except:
        profil = Profil.objects.create(
            user=user, 
            filiere='GL', 
            niveau='L1',
            format_prefere='les_deux'
        )
    
    # Récupérer les compétences et lacunes existantes
    from apps.matching.models import Competence
    from apps.core.models import Matiere
    
    # Compétences existantes (ids des matières)
    competences_existantes = Competence.objects.filter(user=user, type='competence').values_list('matiere_id', flat=True)
    lacunes_existantes = Competence.objects.filter(user=user, type='lacune').values_list('matiere_id', flat=True)
    
    # Récupérer toutes les matières disponibles
    matieres = Matiere.objects.all()
    
    if request.method == 'POST':
        # Mettre à jour les informations générales
        user.prenom = request.POST.get('prenom', user.prenom)
        user.nom = request.POST.get('nom', user.nom)
        user.telephone = request.POST.get('telephone', user.telephone)
        user.save()
        
        # Mettre à jour le profil
        profil.filiere = request.POST.get('filiere', profil.filiere)
        profil.niveau = request.POST.get('niveau', profil.niveau)
        profil.bio = request.POST.get('bio', profil.bio)
        profil.save()
        
        # Supprimer les compétences et lacunes existantes pour éviter les doublons
        Competence.objects.filter(user=user, type='competence').delete()
        Competence.objects.filter(user=user, type='lacune').delete()
        
        # Ajouter les nouvelles compétences
        for matiere_id in request.POST.getlist('competences'):
            if matiere_id:
                Competence.objects.create(
                    user=user,
                    matiere_id=matiere_id,
                    type='competence'
                )
        
        # Ajouter les nouvelles lacunes
        for matiere_id in request.POST.getlist('lacunes'):
            if matiere_id:
                Competence.objects.create(
                    user=user,
                    matiere_id=matiere_id,
                    type='lacune'
                )
        
        messages.success(request, 'Votre profil a été mis à jour !')
        return redirect('profile')
    
    context = {
        'user': user,
        'profil': profil,
        'matieres': matieres,
        'competences_ids': list(competences_existantes),
        'lacunes_ids': list(lacunes_existantes),
    }
    
    return render(request, 'pages/edit_profile.html', context) 
@login_required 
def settings_view(request): 
    return render(request, 'pages/settings.html', {'user': request.user}) 
 
@login_required 
def change_password_view(request): 
    from django.contrib.auth import update_session_auth_hash 
    if request.method == 'POST': 
        old_password = request.POST.get('old_password') 
        new_password = request.POST.get('new_password') 
        confirm_password = request.POST.get('confirm_password') 
        if not request.user.check_password(old_password): 
            messages.error(request, 'Mot de passe actuel incorrect') 
        elif new_password != confirm_password: 
            messages.error(request, 'Les mots de passe ne correspondent pas') 
        elif len(new_password) < 8: 
            messages.error(request, 'Le mot de passe doit contenir au moins 8 caracteres') 
        else: 
            request.user.set_password(new_password) 
            request.user.save() 
            update_session_auth_hash(request, request.user) 
            messages.success(request, 'Mot de passe modifie avec succes') 
        return redirect('settings') 
    return redirect('settings') 
 
@login_required 
def delete_account_view(request): 
    if request.method == 'POST': 
        password = request.POST.get('password') 
        if request.user.check_password(password): 
            request.user.delete() 
            return redirect('home') 
        else: 
            messages.error(request, 'Mot de passe incorrect') 
            return redirect('settings') 
    return redirect('settings') 
