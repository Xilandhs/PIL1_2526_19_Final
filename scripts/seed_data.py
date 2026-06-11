# scripts/seed_data.py
import os
import sys
import django
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta

# Ajouter le chemin du projet
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import Users, Profil
from apps.core.models import Matiere
from apps.matching.models import Competence, Matching, Feedback
from apps.feed.models import Annonce, Candidature
from apps.messaging.models import Messages

def create_matiere():
    """Créer ou récupérer les matières"""
    matieres_data = [
        {'nom': 'Algorithmique', 'categorie': 'Informatique', 'icone': 'code'},
        {'nom': 'Programmation Python', 'categorie': 'Informatique', 'icone': 'terminal'},
        {'nom': 'Bases de données SQL', 'categorie': 'Informatique', 'icone': 'database'},
        {'nom': 'Machine Learning', 'categorie': 'Informatique', 'icone': 'neurology'},
        {'nom': 'Développement Web', 'categorie': 'Informatique', 'icone': 'language'},
        {'nom': 'Mathématiques', 'categorie': 'Mathématiques', 'icone': 'calculate'},
        {'nom': 'Statistiques', 'categorie': 'Mathématiques', 'icone': 'bar_chart'},
        {'nom': 'Réseaux informatiques', 'categorie': 'Informatique', 'icone': 'router'},
        {'nom': 'Cybersécurité', 'categorie': 'Informatique', 'icone': 'security'},
        {'nom': 'Anglais technique', 'categorie': 'Langue', 'icone': 'translate'},
    ]
    
    created = []
    for data in matieres_data:
        matiere, _ = Matiere.objects.get_or_create(nom=data['nom'], defaults=data)
        created.append(matiere)
        print(f"✅ Matière: {matiere.nom}")
    
    return created

def create_users():
    """Créer des utilisateurs de test"""
    users_data = [
        {
            'email': 'thomas.dubois@ifri.bj',
            'prenom': 'Thomas', 'nom': 'Dubois',
            'telephone': '+22961110001', 'sexe': 'M',
            'is_verified': True, 'is_active': True,
            'filiere': 'GL', 'niveau': 'M2',
            'bio': 'Passionné par l\'IA et le machine learning. Je propose des sessions de mentorat en Python, Data Science et Deep Learning.',
            'rating': 4.9, 'nb_avis': 142, 'sessions': 24
        },
        {
            'email': 'sarah.martin@ifri.bj',
            'prenom': 'Sarah', 'nom': 'Martin',
            'telephone': '+22961110002', 'sexe': 'F',
            'is_verified': True, 'is_active': True,
            'filiere': 'IA', 'niveau': 'M1',
            'bio': 'Spécialisée en Data Science. Je peux vous aider en Python, SQL et Machine Learning.',
            'rating': 4.8, 'nb_avis': 98, 'sessions': 18
        },
        {
            'email': 'lucas.kouame@ifri.bj',
            'prenom': 'Lucas', 'nom': 'Kouamé',
            'telephone': '+22961110003', 'sexe': 'M',
            'is_verified': True, 'is_active': True,
            'filiere': 'GL', 'niveau': 'L3',
            'bio': 'Étudiant en génie logiciel, je maîtrise Java, Spring Boot et les bases de données.',
            'rating': 4.7, 'nb_avis': 56, 'sessions': 12
        },
        {
            'email': 'marie.atchade@ifri.bj',
            'prenom': 'Marie', 'nom': 'Atchadé',
            'telephone': '+22961110004', 'sexe': 'F',
            'is_verified': True, 'is_active': True,
            'filiere': 'IM', 'niveau': 'M1',
            'bio': 'Experte en réseaux et cybersécurité. Disponible pour des sessions pratiques.',
            'rating': 4.9, 'nb_avis': 87, 'sessions': 20
        },
        {
            'email': 'jean.adjovi@ifri.bj',
            'prenom': 'Jean', 'nom': 'Adjovi',
            'telephone': '+22961110005', 'sexe': 'M',
            'is_verified': True, 'is_active': True,
            'filiere': 'SI', 'niveau': 'L2',
            'bio': 'Étudiant en L2, je cherche de l\'aide en algorithmique et mathématiques.',
            'rating': 0, 'nb_avis': 0, 'sessions': 0
        },
        {
            'email': 'fatou.sow@ifri.bj',
            'prenom': 'Fatou', 'nom': 'Sow',
            'telephone': '+22961110006', 'sexe': 'F',
            'is_verified': True, 'is_active': True,
            'filiere': 'IA', 'niveau': 'L2',
            'bio': 'Je débute en IA. J\'ai besoin d\'aide en mathématiques et Python.',
            'rating': 0, 'nb_avis': 0, 'sessions': 0
        },
        {
            'email': 'koffi.amegble@ifri.bj',
            'prenom': 'Koffi', 'nom': 'Amegblé',
            'telephone': '+22961110007', 'sexe': 'M',
            'is_verified': True, 'is_active': True,
            'filiere': 'GL', 'niveau': 'L1',
            'bio': 'Nouveau en informatique, je cherche un mentor pour m\'accompagner.',
            'rating': 0, 'nb_avis': 0, 'sessions': 0
        },
        {
            'email': 'elodie.gbesso@ifri.bj',
            'prenom': 'Elodie', 'nom': 'Gbesso',
            'telephone': '+22961110008', 'sexe': 'F',
            'is_verified': True, 'is_active': True,
            'filiere': 'IM', 'niveau': 'L2',
            'bio': 'Je galère en réseaux et C. Besoin d\'un mentor patient.',
            'rating': 0, 'nb_avis': 0, 'sessions': 0
        }
    ]
    
    created_users = []
    for data in users_data:
        username = data['email'].split('@')[0]
        
        user, created = Users.objects.get_or_create(
            email=data['email'],
            defaults={
                'username': username,
                'prenom': data['prenom'],
                'nom': data['nom'],
                'telephone': data['telephone'],
                'sexe': data['sexe'],
                'password': make_password('password123'),
                'is_verified': data['is_verified'],
                'is_active': data['is_active'],
                'rating_moyen': data['rating'],
                'nb_avis': data['nb_avis'],
            }
        )
        
        if created:
            # Créer le profil
            profil, _ = Profil.objects.get_or_create(
                user=user,
                defaults={
                    'filiere': data['filiere'],
                    'niveau': data['niveau'],
                    'bio': data['bio'],
                    'total_sessions': data['sessions'],
                    'format_prefere': 'les_deux'
                }
            )
            print(f"✅ Utilisateur: {user.prenom} {user.nom} ({user.email})")
            created_users.append(user)
        else:
            print(f"⚠️ Utilisateur existe déjà: {user.email}")
    
    return created_users

def create_competences(users, matieres):
    """Créer des compétences et lacunes"""
    
    # Mapping des compétences par utilisateur
    competences_map = {
        'thomas.dubois@ifri.bj': {
            'competences': ['Algorithmique', 'Programmation Python', 'Machine Learning', 'Bases de données SQL'],
            'lacunes': ['Cybersécurité']
        },
        'sarah.martin@ifri.bj': {
            'competences': ['Programmation Python', 'Bases de données SQL', 'Machine Learning', 'Statistiques'],
            'lacunes': ['Développement Web']
        },
        'lucas.kouame@ifri.bj': {
            'competences': ['Algorithmique', 'Programmation Python', 'Bases de données SQL'],
            'lacunes': ['Machine Learning', 'Réseaux informatiques']
        },
        'marie.atchade@ifri.bj': {
            'competences': ['Réseaux informatiques', 'Cybersécurité', 'Algorithmique'],
            'lacunes': ['Machine Learning']
        },
        'jean.adjovi@ifri.bj': {
            'competences': [],
            'lacunes': ['Algorithmique', 'Mathématiques', 'Programmation Python']
        },
        'fatou.sow@ifri.bj': {
            'competences': [],
            'lacunes': ['Mathématiques', 'Programmation Python', 'Statistiques']
        },
        'koffi.amegble@ifri.bj': {
            'competences': [],
            'lacunes': ['Algorithmique', 'Programmation Python', 'Bases de données SQL']
        },
        'elodie.gbesso@ifri.bj': {
            'competences': [],
            'lacunes': ['Réseaux informatiques', 'Algorithmique']
        },
    }
    
    matiere_map = {m.nom: m for m in matieres}
    
    for user in users:
        if user.email in competences_map:
            data = competences_map[user.email]
            
            # Compétences
            for comp_nom in data['competences']:
                if comp_nom in matiere_map:
                    Competence.objects.get_or_create(
                        user=user,
                        matiere=matiere_map[comp_nom],
                        type='competence'
                    )
                    print(f"  📚 {user.prenom} - Compétence: {comp_nom}")
            
            # Lacunes
            for lacune_nom in data['lacunes']:
                if lacune_nom in matiere_map:
                    Competence.objects.get_or_create(
                        user=user,
                        matiere=matiere_map[lacune_nom],
                        type='lacune'
                    )
                    print(f"  🎯 {user.prenom} - Lacune: {lacune_nom}")

# Dans la fonction create_annonces, remplace les valeurs 'offer' et 'request' par 'offre' et 'demande'

def create_annonces(users, matieres):
    """Créer des annonces dans le feed"""
    
    matiere_map = {m.nom: m for m in matieres}
    
    annonces_data = [
        {
            'auteur_email': 'thomas.dubois@ifri.bj',
            'matiere': 'Machine Learning',
            'titre': 'Cours particuliers en Machine Learning',
            'type': 'offre',  # ← changer 'offer' en 'offre'
            'description': 'Je propose des sessions pour comprendre les concepts de base du ML : régression, classification, clustering. Python et scikit-learn au programme.',
            'places_max': 3,
            'format': 'en_ligne'
        },
        {
            'auteur_email': 'sarah.martin@ifri.bj',
            'matiere': 'Programmation Python',
            'titre': 'Aide en Python pour débutants',
            'type': 'offre',  # ← changer 'offer' en 'offre'
            'description': 'Python n\'a plus de secrets pour moi ! Variables, boucles, fonctions, POO. On progresse ensemble à votre rythme.',
            'places_max': 4,
            'format': 'les_deux'
        },
        {
            'auteur_email': 'lucas.kouame@ifri.bj',
            'matiere': 'Algorithmique',
            'titre': 'Besoin d\'aide en algorithmique (L1/L2)',
            'type': 'demande',  # ← changer 'request' en 'demande'
            'description': 'Je galère avec les tris, les récursions et les arbres binaires. Cherche quelqu\'un pour m\'expliquer calmement.',
            'places_max': 1,
            'format': 'en_ligne'
        },
        {
            'auteur_email': 'marie.atchade@ifri.bj',
            'matiere': 'Cybersécurité',
            'titre': 'Initiation à la cybersécurité',
            'type': 'offre',  # ← changer 'offer' en 'offre'
            'description': 'Sécurité des réseaux, chiffrement, bonnes pratiques. Sessions pratiques avec outils réels.',
            'places_max': 2,
            'format': 'presentiel'
        },
        {
            'auteur_email': 'jean.adjovi@ifri.bj',
            'matiere': 'Algorithmique',
            'titre': 'Cherche mentor en algorithmique (urgent)',
            'type': 'demande',  # ← changer 'request' en 'demande'
            'description': 'Examens dans 2 semaines ! Besoin d\'aide urgente pour comprendre les bases.',
            'places_max': 1,
            'format': 'en_ligne'
        },
        {
            'auteur_email': 'fatou.sow@ifri.bj',
            'matiere': 'Mathématiques',
            'titre': 'Aide en maths (probas et stats)',
            'type': 'demande',  # ← changer 'request' en 'demande'
            'description': 'Les probabilités me semblent floues. Cherche quelqu\'un pour m\'aider à préparer mes examens.',
            'places_max': 1,
            'format': 'en_ligne'
        },
    ]
    
    # ... le reste reste identique
def create_matchings(users):
    """Créer des matchings (sessions) entre utilisateurs"""
    
    # Trouver Thomas (mentor) et Jean (mentoré)
    thomas = next((u for u in users if u.email == 'thomas.dubois@ifri.bj'), None)
    jean = next((u for u in users if u.email == 'jean.adjovi@ifri.bj'), None)
    sarah = next((u for u in users if u.email == 'sarah.martin@ifri.bj'), None)
    fatou = next((u for u in users if u.email == 'fatou.sow@ifri.bj'), None)
    
    if thomas and jean:
        matching, created = Matching.objects.get_or_create(
            mentor=thomas,
            mentore=jean,
            defaults={
                'score': 85.5,
                'statut': 'propose',
                'session_date': datetime.now() + timedelta(days=2),
                'duree_minutes': 60,
                'lien_reunion': 'https://meet.google.com/abc-def-ghi'
            }
        )
        if created:
            print(f"✅ Matching: {thomas.prenom} → {jean.prenom} (score: 85.5%)")
    
    if sarah and fatou:
        matching, created = Matching.objects.get_or_create(
            mentor=sarah,
            mentore=fatou,
            defaults={
                'score': 92.0,
                'statut': 'accepte',
                'session_date': datetime.now() + timedelta(days=3),
                'duree_minutes': 90
            }
        )
        if created:
            print(f"✅ Matching: {sarah.prenom} → {fatou.prenom} (score: 92%)")

def create_messages(users):
    """Créer quelques messages de test"""
    
    thomas = next((u for u in users if u.email == 'thomas.dubois@ifri.bj'), None)
    jean = next((u for u in users if u.email == 'jean.adjovi@ifri.bj'), None)
    
    if thomas and jean:
        messages_data = [
            (jean, thomas, "Bonjour Thomas ! J'ai vu que vous êtes expert en algorithmique. Auriez-vous du temps pour m'aider ?"),
            (thomas, jean, "Bonjour Jean ! Bien sûr, je serais ravi de t'aider. Quels sont les concepts qui te posent problème ?"),
            (jean, thomas, "Je bloque surtout sur les arbres binaires et les parcours. Et la récursion me semble abstraite."),
            (thomas, jean, "Pas de souci ! On peut commencer par les bases de la récursion mercredi à 14h ?"),
        ]
        
        for expediteur, destinataire, contenu in messages_data:
            msg, created = Messages.objects.get_or_create(
                expediteur=expediteur,
                destinataire=destinataire,
                contenu=contenu,
                defaults={'created_at': datetime.now() - timedelta(hours=i*2) for i in range(4)}
            )
            if created:
                print(f"💬 Message: {expediteur.prenom} → {destinataire.prenom}")

def run():
    print("=" * 50)
    print("🚀 SEED DATABASE - MENTORLINK")
    print("=" * 50)
    
    print("\n📚 1. Création des matières...")
    matieres = create_matiere()
    
    print("\n👤 2. Création des utilisateurs...")
    users = create_users()
    
    print("\n🎯 3. Ajout des compétences et lacunes...")
    create_competences(users, matieres)
    
    print("\n📢 4. Création des annonces...")
    create_annonces(users, matieres)
    
    print("\n🤝 5. Création des matchings...")
    create_matchings(users)
    
    print("\n💬 6. Création des messages...")
    create_messages(users)
    
    print("\n" + "=" * 50)
    print("✅ SEED TERMINÉ AVEC SUCCÈS !")
    print("=" * 50)
    print("\n📝 Informations de connexion :")
    print("   - Email: thomas.dubois@ifri.bj | Mot de passe: password123")
    print("   - Email: sarah.martin@ifri.bj | Mot de passe: password123")
    print("   - Email: lucas.kouame@ifri.bj | Mot de passe: password123")
    print("   - Email: marie.atchade@ifri.bj | Mot de passe: password123")
    print("   - Email: jean.adjovi@ifri.bj | Mot de passe: password123")
    print("   - Email: fatou.sow@ifri.bj | Mot de passe: password123")
    print("   - Email: koffi.amegble@ifri.bj | Mot de passe: password123")
    print("   - Email: elodie.gbesso@ifri.bj | Mot de passe: password123")

if __name__ == "__main__":
    run()