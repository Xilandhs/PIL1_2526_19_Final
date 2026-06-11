# apps/matching/urls.py
from django.urls import path
from . import views

app_name = 'matching'

urlpatterns = [
    path('', views.matching_view, name='matching'),
    # Supprimer toutes les lignes avec 'sessions'
]