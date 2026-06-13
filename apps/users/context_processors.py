from apps.messaging.models import Messages

def unread_messages(request):
    if request.user.is_authenticated:
        count = Messages.objects.filter(
            destinataire=request.user,
            lu=False
        ).count()
        return {'unread_messages_count': count}
    return {'unread_messages_count': 0}