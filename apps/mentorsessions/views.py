# apps/mentorsessions/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Avg
from django.http import JsonResponse
from datetime import datetime

from apps.matching.models import Matching, Feedback


@login_required
def sessions_list(request):
    """Liste des sessions de l'utilisateur"""
    user = request.user
    
    all_matchings = Matching.objects.filter(Q(mentor=user) | Q(mentore=user))
    
    upcoming = all_matchings.filter(
        statut='accepte',
        session_date__gte=datetime.now()
    ).order_by('session_date')
    
    proposed = all_matchings.filter(statut='propose').order_by('-created_at')
    completed = all_matchings.filter(statut='termine').order_by('-session_date')
    cancelled = all_matchings.filter(statut='refuse').order_by('-updated_at')
    
    for session in completed:
        session.has_feedback = Feedback.objects.filter(matching=session, auteur=user).exists()
    
    total_minutes = completed.aggregate(total=Sum('duree_minutes'))['total'] or 0
    total_hours = total_minutes // 60
    
    avg_rating = Feedback.objects.filter(
        matching__in=completed,
        matching__mentor=user
    ).aggregate(avg=Avg('note'))['avg'] or 0
    
    context = {
        'upcoming_sessions': upcoming,
        'proposed_sessions': proposed,
        'completed_sessions': completed,
        'cancelled_sessions': cancelled,
        'total_hours': total_hours,
        'avg_rating': round(avg_rating, 1),
    }
    return render(request, 'pages/sessions.html', context)


@login_required
def session_detail(request, session_id):
    session = get_object_or_404(
        Matching, 
        id=session_id
    )
    # Vérifier que l'utilisateur est impliqué
    if session.mentor != request.user and session.mentore != request.user:
        return JsonResponse({'error': 'Non autorisé'}, status=403)
    
    other = session.mentore if session.mentor == request.user else session.mentor
    feedback = Feedback.objects.filter(matching=session, auteur=request.user).first()
    
    context = {
        'session': session, 
        'other': other, 
        'feedback': feedback
    }
    return render(request, 'pages/session_detail_modal.html', context)


@login_required
def submit_feedback(request, session_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    
    session = get_object_or_404(
        Matching, 
        id=session_id
    )
    
    # Vérifier que l'utilisateur est impliqué
    if session.mentor != request.user and session.mentore != request.user:
        return JsonResponse({'error': 'Non autorisé'}, status=403)
    
    if session.statut != 'termine':
        return JsonResponse({'error': 'Session non terminée'}, status=400)
    
    if Feedback.objects.filter(matching=session, auteur=request.user).exists():
        return JsonResponse({'error': 'Déjà évalué'}, status=400)
    
    note = request.POST.get('note')
    commentaire = request.POST.get('commentaire', '')
    
    if not note or int(note) < 1 or int(note) > 5:
        return JsonResponse({'error': 'Note invalide'}, status=400)
    
    Feedback.objects.create(
        matching=session,
        auteur=request.user,
        note=note,
        commentaire=commentaire
    )
    
    # Mettre à jour la note moyenne de l'autre personne
    other = session.mentore if session.mentor == request.user else session.mentor
    avg_rating = Feedback.objects.filter(matching__mentor=other).aggregate(avg=Avg('note'))['avg']
    if avg_rating:
        other.rating_moyen = round(avg_rating, 2)
        other.nb_avis = Feedback.objects.filter(matching__mentor=other).count()
        other.save()
    
    return JsonResponse({'success': True})


@login_required
def accept_session(request, session_id):
    session = get_object_or_404(Matching, id=session_id)
    
    if session.mentore != request.user:
        return JsonResponse({'error': 'Non autorisé'}, status=403)
    
    if session.statut != 'propose':
        return JsonResponse({'error': 'Session non proposée'}, status=400)
    
    if request.method == 'POST':
        session.statut = 'accepte'
        session.save()
        messages.success(request, 'Session acceptée !')
    
    return redirect('mentorsessions:list')


@login_required
def cancel_session(request, session_id):
    session = get_object_or_404(Matching, id=session_id)
    
    if session.mentor != request.user and session.mentore != request.user:
        return JsonResponse({'error': 'Non autorisé'}, status=403)
    
    if request.method == 'POST':
        session.statut = 'refuse'
        session.save()
        messages.info(request, 'Session annulée')
    
    return redirect('mentorsessions:list')


@login_required
def complete_session(request, session_id):
    session = get_object_or_404(Matching, id=session_id)
    
    if session.mentor != request.user and session.mentore != request.user:
        return JsonResponse({'error': 'Non autorisé'}, status=403)
    
    if session.statut != 'accepte':
        return JsonResponse({'error': 'Session non acceptée'}, status=400)
    
    if request.method == 'POST':
        session.statut = 'termine'
        session.save()
        
        # Mettre à jour les stats du profil
        try:
            profil = request.user.profil
            profil.total_sessions += 1
            if session.duree_minutes:
                profil.total_heures += session.duree_minutes // 60
            profil.save()
        except:
            pass
        
        messages.success(request, 'Session terminée !')
    
    return redirect('mentorsessions:list')