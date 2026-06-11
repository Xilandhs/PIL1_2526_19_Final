# apps/feed/models.py
from django.db import models
from apps.users.models import Users
from apps.core.models import Matiere, Annonce

class Candidature(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée')
    ]
    
    annonce = models.ForeignKey(
        Annonce, 
        on_delete=models.CASCADE, 
        db_column='annonce_id', 
        related_name='candidatures'
    )
    candidat = models.ForeignKey(
        Users, 
        on_delete=models.CASCADE, 
        db_column='candidat_id', 
        related_name='candidatures'
    )
    messages = models.TextField(blank=True, null=True, db_column='messages')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = False
        db_table = 'candidature'
        unique_together = [['annonce', 'candidat']]
    
    def __str__(self):
        return f"{self.candidat.prenom} {self.candidat.nom} -> {self.annonce.titre}"


class FavoriAnnonce(models.Model):
    user = models.ForeignKey(
        Users, 
        on_delete=models.CASCADE, 
        db_column='user_id', 
        related_name='favoris'
    )
    annonce = models.ForeignKey(
        Annonce, 
        on_delete=models.CASCADE, 
        db_column='annonce_id', 
        related_name='favoris'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'favori_annonce'
        unique_together = [['user', 'annonce']]
    
    def __str__(self):
        return f"{self.user.prenom} {self.user.nom} aime {self.annonce.titre}"