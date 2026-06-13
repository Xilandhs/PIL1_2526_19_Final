from django.core.management.base import BaseCommand
from apps.users.models import Users, Profil
from apps.matching.models import Competence
from apps.core.models import Matiere
import random

class Command(BaseCommand):
    help = 'Crée 20 comptes de test'

    def handle(self, *args, **kwargs):
        comptes = [
            ("Koffi", "Mensah", "koffi.mensah@gmail.com", "GL", "L2"),
            ("Aminata", "Diallo", "aminata.diallo@gmail.com", "IA", "M1"),
            ("Rodrigue", "Ahouansou", "rodrigue.ahouansou@gmail.com", "IM", "L3"),
            ("Fatima", "Saka", "fatima.saka@gmail.com", "SI", "L1"),
            ("Brice", "Tokpo", "brice.tokpo@gmail.com", "GL", "M2"),
            ("Sandrine", "Hounkpe", "sandrine.hounkpe@gmail.com", "IA", "L2"),
            ("Lionel", "Gbeto", "lionel.gbeto@gmail.com", "SEIoT", "L3"),
            ("Merveille", "Agossa", "merveille.agossa@gmail.com", "IM", "M1"),
            ("Patrick", "Dossou", "patrick.dossou@gmail.com", "SI", "L2"),
            ("Christelle", "Akpovo", "christelle.akpovo@gmail.com", "GL", "L1"),
            ("Wilfried", "Houeto", "wilfried.houeto@gmail.com", "IA", "L3"),
            ("Nadege", "Gbenou", "nadege.gbenou@gmail.com", "IM", "M2"),
            ("Ulrich", "Azonhiho", "ulrich.azonhiho@gmail.com", "SEIoT", "L2"),
            ("Raissa", "Biokou", "raissa.biokou@gmail.com", "GL", "M1"),
            ("Fernand", "Tchegnon", "fernand.tchegnon@gmail.com", "SI", "L3"),
            ("Ornella", "Vodounou", "ornella.vodounou@gmail.com", "IA", "L1"),
            ("Geraud", "Sossou", "geraud.sossou@gmail.com", "IM", "L2"),
            ("Prudence", "Adjovi", "prudence.adjovi@gmail.com", "GL", "M1"),
            ("Maxime", "Hounkanrin", "maxime.hounkanrin@gmail.com", "SEIoT", "L3"),
            ("Deborah", "Zannou", "deborah.zannou@gmail.com", "SI", "M2"),
        ]

        matieres_comp = ["Algorithmique", "Programmation Python", "Bases de données SQL", "Machine Learning", "Développement Web"]
        matieres_lacune = ["Mathématiques", "Statistiques", "Réseaux informatiques", "Cybersécurité", "Anglais technique"]

        for i, (prenom, nom, email, filiere, niveau) in enumerate(comptes):
            if Users.objects.filter(email=email).exists():
                self.stdout.write(f'⚠ {prenom} {nom} existe déjà')
                continue
            try:
                user = Users.objects.create_user(
                    username=email,
                    email=email,
                    password="Mentorlink2026",
                    prenom=prenom,
                    nom=nom,
                    telephone=f"022{i:07d}",
                    sexe="F" if i % 2 == 0 else "M",
                    is_active=True
                )
                Profil.objects.create(
                    user=user,
                    filiere=filiere,
                    niveau=niveau,
                    format_prefere="les_deux",
                    bio=f"Etudiant(e) en {filiere} niveau {niveau} a l'IFRI."
                )
                for mat_nom in random.sample(matieres_comp, 2):
                    mat, _ = Matiere.objects.get_or_create(nom=mat_nom)
                    Competence.objects.get_or_create(user=user, matiere=mat, defaults={"type": "competence"})
                for mat_nom in random.sample(matieres_lacune, 2):
                    mat, _ = Matiere.objects.get_or_create(nom=mat_nom)
                    Competence.objects.get_or_create(user=user, matiere=mat, defaults={"type": "lacune"})
                self.stdout.write(f'✓ {prenom} {nom} créé')
            except Exception as e:
                self.stdout.write(f'✗ {prenom} {nom} : {e}')

        self.stdout.write('Terminé !')