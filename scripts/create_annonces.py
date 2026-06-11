# scripts/create_annonces.py
import os
import sys
import django
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import Users
from apps.core.models import Matiere
from apps.feed.models import Annonce, Candidature, FavoriAnnonce

def create_annonces():
    """Créer les annonces avec les vrais utilisateurs"""
    
    print("=" * 60)
    print("🚀 CRÉATION DES ANNONCES - MENTORLINK")
    print("=" * 60)
    
    # Récupérer les utilisateurs
    print("\n📋 Récupération des utilisateurs...")
    thomas = Users.objects.get(email='thomas.dubois@ifri.bj')
    sarah = Users.objects.get(email='sarah.martin@ifri.bj')
    lucas = Users.objects.get(email='lucas.kouame@ifri.bj')
    marie = Users.objects.get(email='marie.atchade@ifri.bj')
    jean = Users.objects.get(email='jean.adjovi@ifri.bj')
    fatou = Users.objects.get(email='fatou.sow@ifri.bj')
    koffi = Users.objects.get(email='koffi.amegble@ifri.bj')
    elodie = Users.objects.get(email='elodie.gbesso@ifri.bj')
    print(f"   ✅ {thomas.prenom} {thomas.nom}")
    print(f"   ✅ {sarah.prenom} {sarah.nom}")
    print(f"   ✅ {lucas.prenom} {lucas.nom}")
    print(f"   ✅ {marie.prenom} {marie.nom}")
    print(f"   ✅ {jean.prenom} {jean.nom}")
    print(f"   ✅ {fatou.prenom} {fatou.nom}")
    print(f"   ✅ {koffi.prenom} {koffi.nom}")
    print(f"   ✅ {elodie.prenom} {elodie.nom}")
    
    # Récupérer les matières
    print("\n📚 Récupération des matières...")
    algo = Matiere.objects.get(nom='Algorithmique')
    python = Matiere.objects.get(nom='Programmation Python')
    sql = Matiere.objects.get(nom='Bases de données SQL')
    maths = Matiere.objects.get(nom='Mathématiques')
    reseaux = Matiere.objects.get(nom='Réseaux informatiques')
    cybersecurite = Matiere.objects.get(nom='Cybersécurité')
    print(f"   ✅ {algo.nom}")
    print(f"   ✅ {python.nom}")
    print(f"   ✅ {sql.nom}")
    print(f"   ✅ {maths.nom}")
    print(f"   ✅ {reseaux.nom}")
    print(f"   ✅ {cybersecurite.nom}")
    
    # Supprimer les anciennes annonces
    print("\n🗑️ Suppression des anciennes annonces...")
    deleted_count = Annonce.objects.all().delete()[0]
    print(f"   ✅ {deleted_count} annonces supprimées")
    
    annonces_data = [
        {
            'auteur': thomas,
            'matiere': algo,
            'titre': 'Aide pour les TPs d\'algorithmique',
            'type': 'offre',
            'format': 'les_deux',
            'description': """Je propose de l'aide pour les TPs d'algo et la structure de données. 
J'ai validé ces modules avec 18/20 et je peux expliquer patiemment les concepts de pointeurs, 
complexité algorithmique et structures de données avancées.""",
            'places_max': 3,
            'created_at': datetime.now() - timedelta(hours=2)
        },
        {
            'auteur': sarah,
            'matiere': python,
            'titre': 'Aide en Python pour débutants',
            'type': 'offre',
            'format': 'en_ligne',
            'description': """Python n'a plus de secrets pour moi ! Variables, boucles, fonctions, POO. 
On progresse ensemble à votre rythme.""",
            'places_max': 4,
            'created_at': datetime.now() - timedelta(hours=5)
        },
        {
            'auteur': lucas,
            'matiere': algo,
            'titre': 'Besoin d\'aide en algorithmique (L1/L2)',
            'type': 'demande',
            'format': 'en_ligne',
            'description': """Je galère avec les tris, les récursions et les arbres binaires. 
Cherche quelqu'un pour m'expliquer calmement avant les examens.""",
            'places_max': 1,
            'created_at': datetime.now() - timedelta(days=1)
        },
        {
            'auteur': marie,
            'matiere': cybersecurite,
            'titre': 'Initiation à la cybersécurité',
            'type': 'offre',
            'format': 'presentiel',
            'description': """Sécurité des réseaux, chiffrement, bonnes pratiques. 
Sessions pratiques avec outils réels.""",
            'places_max': 2,
            'created_at': datetime.now() - timedelta(days=1)
        },
        {
            'auteur': jean,
            'matiere': algo,
            'titre': 'Cherche mentor en algorithmique (urgent)',
            'type': 'demande',
            'format': 'en_ligne',
            'description': """Examens dans 2 semaines ! Besoin d'aide urgente pour comprendre les bases 
de l'algorithmique et des structures de données.""",
            'places_max': 1,
            'created_at': datetime.now() - timedelta(days=2)
        },
        {
            'auteur': fatou,
            'matiere': maths,
            'titre': 'Aide en maths (probas et stats)',
            'type': 'demande',
            'format': 'en_ligne',
            'description': """Les probabilités me semblent floues. 
Cherche quelqu'un pour m'aider à préparer mes examens de statistiques.""",
            'places_max': 1,
            'created_at': datetime.now() - timedelta(days=2)
        },
        {
            'auteur': koffi,
            'matiere': sql,
            'titre': 'Besoin d\'aide en SQL - Débutant',
            'type': 'demande',
            'format': 'en_ligne',
            'description': """Je débute en SQL et j'ai du mal avec les jointures et les sous-requêtes. 
Cherche un mentor patient pour m'accompagner.""",
            'places_max': 1,
            'created_at': datetime.now() - timedelta(days=3)
        },
        {
            'auteur': elodie,
            'matiere': reseaux,
            'titre': 'Aide en réseaux informatiques',
            'type': 'demande',
            'format': 'presentiel',
            'description': """Je bloque sur le modèle OSI, TCP/IP et le routage. 
J'aurais besoin de quelqu'un pour m'expliquer concrètement.""",
            'places_max': 1,
            'created_at': datetime.now() - timedelta(days=3)
        }
    ]
    
    print("\n📢 Création des annonces...")
    created_annonces = []
    for data in annonces_data:
        annonce, created = Annonce.objects.get_or_create(
            auteur=data['auteur'],
            titre=data['titre'],
            defaults={
                'matiere': data['matiere'],
                'type': data['type'],
                'format': data['format'],
                'description': data['description'],
                'places_max': data['places_max'],
                'places_restantes': data['places_max'],
                'created_at': data['created_at']
            }
        )
        if created:
            created_annonces.append(annonce)
            print(f"   ✅ Annonce {len(created_annonces)}: {annonce.titre} par {annonce.auteur.prenom} {annonce.auteur.nom}")
    
    # Ajouter des likes sur certaines annonces
    print("\n❤️ Ajout des likes...")
    
    annonce_sarah = Annonce.objects.filter(auteur=sarah).first()
    if annonce_sarah:
        FavoriAnnonce.objects.get_or_create(user=thomas, annonce=annonce_sarah)
        annonce_sarah.likes = FavoriAnnonce.objects.filter(annonce=annonce_sarah).count()
        annonce_sarah.save()
        print(f"   ✅ {thomas.prenom} a liké l'annonce de {sarah.prenom}")
    
    annonce_thomas = Annonce.objects.filter(auteur=thomas, type='offre').first()
    if annonce_thomas:
        FavoriAnnonce.objects.get_or_create(user=sarah, annonce=annonce_thomas)
        annonce_thomas.likes = FavoriAnnonce.objects.filter(annonce=annonce_thomas).count()
        annonce_thomas.save()
        print(f"   ✅ {sarah.prenom} a liké l'annonce de {thomas.prenom}")
    
    annonce_marie = Annonce.objects.filter(auteur=marie).first()
    if annonce_marie:
        FavoriAnnonce.objects.get_or_create(user=lucas, annonce=annonce_marie)
        annonce_marie.likes = FavoriAnnonce.objects.filter(annonce=annonce_marie).count()
        annonce_marie.save()
        print(f"   ✅ {lucas.prenom} a liké l'annonce de {marie.prenom}")
    
    # Ajouter des candidatures
    print("\n📝 Ajout des candidatures...")
    
    # Jean postule à l'annonce de Thomas
    if annonce_thomas and jean:
        candidature, created = Candidature.objects.get_or_create(
            annonce=annonce_thomas,
            candidat=jean,
            defaults={
                'statut': 'en_attente',
                'messages': "Bonjour Thomas, je suis intéressé par votre aide en algorithmique."
            }
        )
        if created:
            print(f"   ✅ {jean.prenom} a postulé à l'annonce de {thomas.prenom}")
        else:
            print(f"   ⚠️ {jean.prenom} a déjà postulé à l'annonce de {thomas.prenom}")
    
    # Fatou postule à l'annonce de Sarah
    if annonce_sarah and fatou:
        candidature, created = Candidature.objects.get_or_create(
            annonce=annonce_sarah,
            candidat=fatou,
            defaults={
                'statut': 'en_attente',
                'messages': "Bonjour Sarah, j'aimerais progresser en Python."
            }
        )
        if created:
            print(f"   ✅ {fatou.prenom} a postulé à l'annonce de {sarah.prenom}")
        else:
            print(f"   ⚠️ {fatou.prenom} a déjà postulé à l'annonce de {sarah.prenom}")
    
    print("\n" + "=" * 60)
    print(f"✅ {len(created_annonces)} annonces créées avec succès !")
    print("=" * 60)
    
    return created_annonces

if __name__ == "__main__":
    create_annonces()