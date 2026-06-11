# apps/messaging/models.py
from django.db import models
from apps.users.models import Users
from apps.core.models import Annonce

class Messages(models.Model):
    expediteur = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='expediteur_id', related_name='messages_envoyes')
    destinataire = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='destinataire_id', related_name='messages_recus')
    contenu = models.TextField()
    lu = models.BooleanField(default=False)
    lu_at = models.DateTimeField(blank=True, null=True)
    message_reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, db_column='message_reply_to', blank=True, null=True)
    matching = models.ForeignKey('matching.Matching', on_delete=models.SET_NULL, blank=True, null=True)
    annonce = models.ForeignKey(Annonce, on_delete=models.SET_NULL, blank=True, null=True)
    est_modifie = models.BooleanField(default=False)
    est_supprime = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'messages'  # ← Important : nom exact de la table dans PostgreSQL
        ordering = ['created_at']


class PieceJointe(models.Model):
    message = models.ForeignKey(Messages, on_delete=models.CASCADE, db_column='message_id', related_name='pieces_jointes')
    nom_fichier = models.CharField(max_length=255)
    url_fichier = models.CharField(max_length=500)
    type_fichier = models.CharField(max_length=50, blank=True, null=True)
    taille = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'piece_jointe'


class ReactionMessage(models.Model):
    message = models.ForeignKey(Messages, on_delete=models.CASCADE, db_column='message_id', related_name='reactions')
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    emoji = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'reaction_message'
        unique_together = [['message', 'user', 'emoji']]