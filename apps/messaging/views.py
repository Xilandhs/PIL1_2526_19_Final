# apps/messaging/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.core.cache import cache
import time

from apps.users.models import Users
from apps.messaging.models import Messages

# Constante pour le timeout de l'indicateur de saisie (secondes)
TYPING_TIMEOUT = 3


@login_required
def conversations_list(request):
    """Liste des conversations de l'utilisateur"""
    user = request.user
    
    # Récupérer tous les utilisateurs avec qui on a échangé
    destinataires_ids = Messages.objects.filter(expediteur=user).values_list('destinataire_id', flat=True).distinct()
    expediteurs_ids = Messages.objects.filter(destinataire=user).values_list('expediteur_id', flat=True).distinct()
    all_contact_ids = set(destinataires_ids) | set(expediteurs_ids)
    
    # Récupérer les utilisateurs contacts
    contacts = Users.objects.filter(id__in=all_contact_ids)
    
    conversations = []
    for contact in contacts:
        # Dernier message
        last_message = Messages.objects.filter(
            (Q(expediteur=user, destinataire=contact) |
             Q(expediteur=contact, destinataire=user))
        ).order_by('-created_at').first()
        
        # Compter les messages non lus
        unread_count = Messages.objects.filter(
            expediteur=contact,
            destinataire=user,
            lu=False
        ).count()
        
        conversations.append({
            'contact': contact,
            'last_message': last_message,
            'unread_count': unread_count
        })
    
    # Trier par dernier message
    conversations.sort(
        key=lambda x: x['last_message'].created_at if x['last_message'] else '',
        reverse=True
    )
    
    # Conversation sélectionnée
    contact_id = request.GET.get('contact')
    contact = None
    messages_list = []
    
    if contact_id:
        # Empêcher de converser avec soi-même
        if int(contact_id) == user.id:
            return redirect('/chat/')
        
        contact = get_object_or_404(Users, id=contact_id)
        messages_list = Messages.objects.filter(
            (Q(expediteur=user, destinataire=contact) |
             Q(expediteur=contact, destinataire=user))
        ).order_by('created_at')
        
        # Marquer comme lus
        Messages.objects.filter(
            expediteur=contact,
            destinataire=user,
            lu=False
        ).update(lu=True)
    
    context = {
        'conversations': conversations,
        'contact': contact,
        'messages': messages_list,
    }
    return render(request, 'pages/chat.html', context)


@login_required
def send_message(request, user_id):
    """Envoyer un message"""
    if request.method == 'POST':
        user = request.user
        
        # Empêcher d'envoyer un message à soi-même
        if user.id == int(user_id):
            return JsonResponse({'success': False, 'error': 'Vous ne pouvez pas vous envoyer un message à vous-même'})
        
        contact = get_object_or_404(Users, id=user_id)
        contenu = request.POST.get('contenu', '').strip()
        
        if contenu:
            message = Messages.objects.create(
                expediteur=user,
                destinataire=contact,
                contenu=contenu
            )
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': {
                        'id': message.id,
                        'contenu': message.contenu,
                        'created_at': message.created_at.strftime('%H:%M'),
                        'is_sent': True
                    }
                })
        
        return redirect(f'/chat/?contact={contact.id}')
    
    return redirect('chat')


@login_required
def get_new_messages(request, user_id):
    """Récupérer les nouveaux messages (polling)"""
    user = request.user
    
    # Empêcher de surveiller ses propres messages
    if user.id == int(user_id):
        return JsonResponse({'messages': [], 'is_typing': False})
    
    contact = get_object_or_404(Users, id=user_id)
    last_id = request.GET.get('last_id', 0)
    
    # Récupérer les nouveaux messages
    new_messages = Messages.objects.filter(
        expediteur=contact,
        destinataire=user,
        id__gt=last_id
    ).order_by('created_at')
    
    # Marquer comme lus
    new_messages.update(lu=True)
    
    messages_data = []
    for msg in new_messages:
        messages_data.append({
            'id': msg.id,
            'contenu': msg.contenu,
            'created_at': msg.created_at.strftime('%H:%M'),
            'is_sent': False
        })
    
    # Vérifier si le contact est en train d'écrire
    is_typing = False
    typing_key = f"typing_{contact.id}_to_{user.id}"
    typing_time = cache.get(typing_key)
    if typing_time:
        is_typing = (time.time() - typing_time) < TYPING_TIMEOUT
    
    return JsonResponse({
        'messages': messages_data,
        'is_typing': is_typing
    })


@login_required
def typing_indicator(request, user_id):
    """Indique que l'utilisateur courant est en train d'écrire"""
    # Empêcher l'auto-indication
    if request.user.id == int(user_id):
        return JsonResponse({'status': 'ok'})
    
    key = f"typing_{request.user.id}_to_{user_id}"
    cache.set(key, time.time(), TYPING_TIMEOUT)
    return JsonResponse({'status': 'ok'})


@login_required
def stop_typing(request, user_id):
    """Arrête l'indicateur de saisie"""
    key = f"typing_{request.user.id}_to_{user_id}"
    cache.delete(key)
    return JsonResponse({'status': 'ok'})


@login_required
def new_conversation(request):
    """Page pour démarrer une nouvelle conversation"""
    user = request.user
    
    # Récupérer tous les utilisateurs sauf soi-même
    users = Users.objects.exclude(id=user.id).order_by('prenom')
    
    # Récupérer les IDs des utilisateurs avec qui on a déjà conversé
    existing_conversations = set()
    for contact in users:
        if Messages.objects.filter(
            (Q(expediteur=user, destinataire=contact) | 
             Q(expediteur=contact, destinataire=user))
        ).exists():
            existing_conversations.add(contact.id)
    
    context = {
        'users': users,
        'existing_conversations': existing_conversations,
    }
    return render(request, 'pages/new_conversation.html', context)


@login_required
def get_users_list(request):
    """API pour récupérer la liste des utilisateurs (AJAX)"""
    search = request.GET.get('search', '')
    user = request.user
    
    users = Users.objects.exclude(id=user.id)
    if search:
        users = users.filter(
            Q(prenom__icontains=search) | 
            Q(nom__icontains=search) | 
            Q(email__icontains=search)
        )
    
    users_data = []
    for u in users[:20]:
        users_data.append({
            'id': u.id,
            'prenom': u.prenom,
            'nom': u.nom,
            'avatar': u.profil.photo_url if hasattr(u, 'profil') and u.profil.photo_url else None,
            'initials': f"{u.prenom[0]}{u.nom[0]}",
    
        })
    
    return JsonResponse({'users': users_data})


@login_required
def conversation_with(request, user_id):
    """Démarrer ou continuer une conversation avec un utilisateur spécifique"""
    user = request.user
    
    # Empêcher de converser avec soi-même
    if user.id == int(user_id):
        return redirect('/chat/')
    
    contact = get_object_or_404(Users, id=user_id)
    
    # Rediriger vers la page de conversation avec ce contact
    return redirect(f'/chat/?contact={contact.id}')

# apps/messaging/views.py

def legacy_redirect(request, user_id):
    """Redirige les anciennes URLs /chat/new/<id>/ vers /chat/with/<id>/"""
    return redirect(f'/chat/with/{user_id}/')