# apps/users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=150)
    telephone = models.CharField(unique=True, max_length=20)
    matricule = models.CharField(unique=True, max_length=50, blank=True, null=True)
    statut = models.CharField(max_length=20, default='deconnecte')
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    rating_moyen = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    nb_avis = models.IntegerField(default=0)
    last_seen = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nom', 'prenom', 'telephone']
    
    class Meta:
        managed = False
        db_table = 'users'
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Profil(models.Model):
    FILIERE_CHOICES = [
        ('IA', 'IA'), 
        ('IM', 'IM'), 
        ('GL', 'GL'), 
        ('SEIoT', 'SEIoT'), 
        ('SI', 'SI')
    ]
    NIVEAU_CHOICES = [
        ('L1', 'Licence 1'), 
        ('L2', 'Licence 2'), 
        ('L3', 'Licence 3'), 
        ('M1', 'Master 1'), 
        ('M2', 'Master 2')
    ]
    FORMAT_CHOICES = [
        ('presentiel', 'Présentiel'), 
        ('en_ligne', 'En ligne'), 
        ('les_deux', 'Les deux')
    ]
    
    user = models.OneToOneField(Users, on_delete=models.CASCADE, db_column='user_id')
    filiere = models.CharField(max_length=10, choices=FILIERE_CHOICES)
    niveau = models.CharField(max_length=2, choices=NIVEAU_CHOICES)
    bio = models.TextField(blank=True, null=True)
    photo_url = models.CharField(max_length=500, blank=True, null=True)
    banner_url = models.CharField(max_length=500, blank=True, null=True)
    format_prefere = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='les_deux')
    response_rate = models.IntegerField(blank=True, null=True, default=0)
    avg_response_time = models.IntegerField(blank=True, null=True, default=0)
    total_sessions = models.IntegerField(blank=True, null=True, default=0)
    total_heures = models.IntegerField(blank=True, null=True, default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = False
        db_table = 'profil'


class Disponibilite(models.Model):
    JOURS = [
        ('Lundi', 'Lundi'), 
        ('Mardi', 'Mardi'), 
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'), 
        ('Vendredi', 'Vendredi'), 
        ('Samedi', 'Samedi'),
        ('Dimanche', 'Dimanche')
    ]
    
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    jour = models.CharField(max_length=10, choices=JOURS)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    est_recurrent = models.BooleanField(default=True)
    
    class Meta:
        managed = False
        db_table = 'disponibilite'