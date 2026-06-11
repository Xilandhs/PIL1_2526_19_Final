# apps/feed/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from apps.core.models import Matiere
from apps.feed.models import Annonce, Candidature, FavoriAnnonce


@login_required
def feed_view(request):
    """Page principale du feed avec toutes les annonces"""
    user = request.user
    
    subject_filter = request.GET.get('subject', 'all')
    type_filter = request.GET.get('type', 'all')
    availability_filter = request.GET.get('availability', 'all')
    
    annonces = Annonce.objects.filter(statut='active').order_by('-created_at')
    
    if subject_filter != 'all':
        annonces = annonces.filter(matiere_id=subject_filter)
    
    if type_filter != 'all':
        annonces = annonces.filter(type=type_filter)
    
    if availability_filter != 'all':
        if availability_filter == 'online':
            annonces = annonces.filter(format='en_ligne')
        elif availability_filter == 'onsite':
            annonces = annonces.filter(format='presentiel')
    
    matieres = Matiere.objects.all()
    
    for annonce in annonces:
        annonce.user_has_liked = FavoriAnnonce.objects.filter(user=user, annonce=annonce).exists()
    
    context = {
        'annonces': annonces,
        'matieres': matieres,
        'subject_filter': subject_filter,
        'type_filter': type_filter,
        'availability_filter': availability_filter,
    }
    
    return render(request, 'pages/feed.html', context)


@login_required
def create_annonce(request):
    """Créer une nouvelle annonce"""
    if request.method == 'POST':
        titre = request.POST.get('titre')
        matiere_id = request.POST.get('matiere')
        type_annonce = request.POST.get('type')
        description = request.POST.get('description')
        format_annonce = request.POST.get('format')
        places_max = request.POST.get('places_max', 1)
        
        if not titre or not matiere_id or not description:
            messages.error(request, 'Veuillez remplir tous les champs obligatoires')
            return redirect('my_feed')
        
        matiere = get_object_or_404(Matiere, id=matiere_id)
        
        Annonce.objects.create(
            auteur=request.user,
            matiere=matiere,
            titre=titre,
            type=type_annonce,
            description=description,
            format=format_annonce,
            places_max=places_max,
            places_restantes=places_max
        )
        
        messages.success(request, 'Annonce publiée avec succès !')
        return redirect('my_feed')
    
    return redirect('my_feed')


@login_required
def toggle_like(request, annonce_id):
    """Liker/Unliker une annonce"""
    annonce = get_object_or_404(Annonce, id=annonce_id)
    like, created = FavoriAnnonce.objects.get_or_create(user=request.user, annonce=annonce)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    annonce.likes = FavoriAnnonce.objects.filter(annonce=annonce).count()
    annonce.save()
    
    return JsonResponse({'liked': liked, 'likes_count': annonce.likes})


@login_required
def apply_to_annonce(request, annonce_id):
    """Postuler à une annonce"""
    annonce = get_object_or_404(Annonce, id=annonce_id, statut='active')
    
    if request.method == 'POST':
        message_candidature = request.POST.get('message', '')
        
        if Candidature.objects.filter(annonce=annonce, candidat=request.user).exists():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Vous avez déjà postulé'})
            messages.warning(request, 'Vous avez déjà postulé')
            return redirect('feed')
        
        Candidature.objects.create(
            annonce=annonce,
            candidat=request.user,
            messages=message_candidature,
            statut='en_attente'
        )
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        
        messages.success(request, 'Candidature envoyée !')
        return redirect('feed')
    
    return redirect('feed')


@login_required
def get_candidature_form(request, annonce_id):
    """Récupérer les infos d'une annonce pour la modal"""
    annonce = get_object_or_404(Annonce, id=annonce_id)
    return JsonResponse({
        'id': annonce.id,
        'titre': annonce.titre,
        'auteur': f"{annonce.auteur.prenom} {annonce.auteur.nom}",
        'places_restantes': annonce.places_restantes,
    })


@login_required
def my_ads_view(request):
    """Page Mes annonces"""
    user = request.user
    user_ads = Annonce.objects.filter(auteur=user).order_by('-created_at')
    
    # Statistiques
    active_ads = user_ads.filter(statut='active')
    total_views = sum(ad.vues for ad in user_ads)
    total_candidatures = sum(ad.candidatures.count() for ad in user_ads)
    
    # Taux de réponse fictif (à calculer selon tes besoins)
    response_rate = 94
    
    context = {
        'user_ads': user_ads,
        'active_ads': active_ads,
        'total_views': total_views,
        'total_candidatures': total_candidatures,
        'response_rate': response_rate,
        'matieres': Matiere.objects.all(),
    }
    return render(request, 'pages/my-announcements.html', context)


@login_required
def get_annonce_json(request, annonce_id):
    """Récupérer une annonce en JSON pour édition"""
    annonce = get_object_or_404(Annonce, id=annonce_id, auteur=request.user)
    return JsonResponse({
        'id': annonce.id,
        'titre': annonce.titre,
        'type': annonce.type,
        'matiere_id': annonce.matiere_id,
        'description': annonce.description,
        'format': annonce.format,
        'places_max': annonce.places_max,
    })


@login_required
def edit_annonce(request, annonce_id):
    """Modifier une annonce"""
    annonce = get_object_or_404(Annonce, id=annonce_id, auteur=request.user)
    
    if request.method == 'POST':
        annonce.titre = request.POST.get('titre', annonce.titre)
        annonce.matiere_id = request.POST.get('matiere', annonce.matiere_id)
        annonce.type = request.POST.get('type', annonce.type)
        annonce.description = request.POST.get('description', annonce.description)
        annonce.format = request.POST.get('format', annonce.format)
        annonce.places_max = request.POST.get('places_max', annonce.places_max)
        annonce.save()
        
        messages.success(request, 'Annonce modifiée avec succès !')
        return redirect('my_feed')
    
    return redirect('my_feed')


@login_required
def archive_annonce(request, annonce_id):
    """Archiver ou restaurer une annonce"""
    annonce = get_object_or_404(Annonce, id=annonce_id, auteur=request.user)
    
    if request.method == 'POST':
        if annonce.statut == 'active':
            annonce.statut = 'archivee'
        else:
            annonce.statut = 'active'
        annonce.save()
        return JsonResponse({'success': True, 'new_status': annonce.statut})
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


@login_required
def delete_annonce(request, annonce_id):
    """Supprimer définitivement une annonce"""
    annonce = get_object_or_404(Annonce, id=annonce_id, auteur=request.user)
    
    if request.method == 'POST':
        annonce.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)