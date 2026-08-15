from datetime import date, timedelta

from src.models.mouvement import Mouvement, TypeMouvement
from src.repositories.mouvement_repository import MouvementRepository


def inserer_donnees_demo(repo: MouvementRepository) -> None:
    """Insère un jeu de données fictif, pour la démonstration publique uniquement."""
    aujourdhui = date.today()

    mouvements_demo = [
        Mouvement(date=aujourdhui - timedelta(days=28), montant=180000, type=TypeMouvement.ENTREE, note="Mission freelance"),
        Mouvement(date=aujourdhui - timedelta(days=25), montant=15000, type=TypeMouvement.DEPENSE, categorie="Nourriture", note="Courses du mois"),
        Mouvement(date=aujourdhui - timedelta(days=24), montant=8000, type=TypeMouvement.DEPENSE, categorie="Transport"),
        Mouvement(date=aujourdhui - timedelta(days=20), montant=20000, type=TypeMouvement.EPARGNE),
        Mouvement(date=aujourdhui - timedelta(days=18), montant=12000, type=TypeMouvement.DEPENSE, categorie="Loisirs", note="Sortie entre amis"),
        Mouvement(date=aujourdhui - timedelta(days=14), montant=95000, type=TypeMouvement.ENTREE, note="Vente d'un article"),
        Mouvement(date=aujourdhui - timedelta(days=10), montant=6000, type=TypeMouvement.DEPENSE, categorie="Transport"),
        Mouvement(date=aujourdhui - timedelta(days=8), montant=25000, type=TypeMouvement.DEPENSE, categorie="Nourriture"),
        Mouvement(date=aujourdhui - timedelta(days=5), montant=15000, type=TypeMouvement.EPARGNE),
        Mouvement(date=aujourdhui - timedelta(days=2), montant=4500, type=TypeMouvement.DEPENSE, categorie="Loisirs", note="Cinéma"),
    ]

    for mouvement in mouvements_demo:
        repo.ajouter(mouvement)