# apps/matching/models.py
from django.db import models
from apps.users.models import Users
from apps.core.models import Matiere, Annonce

class Competence(models.Model):
    TYPE_CHOICES = [('competence', 'Compétence'), ('lacune', 'Lacune')]
    
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id', related_name='competences')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, db_column='matiere_id')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    niveau = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'competence'
        unique_together = [['user', 'matiere', 'type']]


class Matching(models.Model):
    STATUT_CHOICES = [('propose', 'Proposé'), ('accepte', 'Accepté'), ('refuse', 'Refusé'), ('termine', 'Terminé')]
    
    mentor = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='mentor_id', related_name='matchings_mentor')
    mentore = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='mentore_id', related_name='matchings_mentore')
    annonce = models.ForeignKey(Annonce, on_delete=models.SET_NULL, db_column='annonce_id', blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='propose')
    session_date = models.DateTimeField(blank=True, null=True)
    duree_minutes = models.IntegerField(default=60)
    lien_reunion = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = False
        db_table = 'matching'
        unique_together = [['mentor', 'mentore', 'annonce']]


class Feedback(models.Model):
    matching = models.ForeignKey(Matching, on_delete=models.CASCADE, db_column='matching_id')
    auteur = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='auteur_id')
    note = models.IntegerField()
    commentaire = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'feedback'
        unique_together = [['matching', 'auteur']]