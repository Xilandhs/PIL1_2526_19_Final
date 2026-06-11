# apps/core/models.py
from django.db import models
from apps.users.models import Users

class Matiere(models.Model):
    nom = models.CharField(unique=True, max_length=150)
    categorie = models.CharField(max_length=100, blank=True, null=True)
    filiere_cible = models.CharField(max_length=100, blank=True, null=True)
    icone = models.CharField(max_length=50, default='school')
    couleur = models.CharField(max_length=20, default='#386943')
    
    class Meta:
        managed = False
        db_table = 'matiere'
    
    def __str__(self):
        return self.nom


class Annonce(models.Model):
    TYPE_CHOICES = [('offre', 'Offre'), ('demande', 'Demande')]
    FORMAT_CHOICES = [('presentiel', 'Présentiel'), ('en_ligne', 'En ligne'), ('les_deux', 'Les deux')]
    STATUT_CHOICES = [('active', 'Active'), ('archivee', 'Archivée'), ('fermee', 'Fermée')]
    
    auteur = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='auteur_id', related_name='annonces')
    matiere = models.ForeignKey(Matiere, on_delete=models.PROTECT, db_column='matiere_id')
    titre = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='les_deux')
    description = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='active')
    places_max = models.IntegerField(default=1)
    places_restantes = models.IntegerField(default=1)
    likes = models.IntegerField(default=0)
    vues = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = False
        db_table = 'annonce'