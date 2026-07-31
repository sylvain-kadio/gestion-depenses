import pytest
from datetime import date

from src.database.connexion import initialiser_base
from src.repositories.mouvement_repository import MouvementRepository
from src.services.calculateur_solde import CalculateurSolde
from src.models.mouvement import Mouvement, TypeMouvement


@pytest.fixture
def calculateur(tmp_path):
    chemin_base = tmp_path / "test.db"
    initialiser_base(chemin_base)
    repo = MouvementRepository(chemin_base)
    return CalculateurSolde(repo), repo


def test_solde_periode_soustrait_depenses_et_epargne(calculateur):
    calc, repo = calculateur
    repo.ajouter(Mouvement(date=date(2026, 7, 15), montant=50000, type=TypeMouvement.ENTREE))
    repo.ajouter(Mouvement(date=date(2026, 7, 15), montant=5000, type=TypeMouvement.DEPENSE, categorie="nourriture"))
    repo.ajouter(Mouvement(date=date(2026, 7, 15), montant=10000, type=TypeMouvement.EPARGNE))

    solde = calc.solde_periode(date(2026, 7, 1), date(2026, 7, 31))

    assert solde == 35000


def test_solde_periode_ignore_les_mouvements_hors_plage(calculateur):
    calc, repo = calculateur
    repo.ajouter(Mouvement(date=date(2026, 7, 15), montant=50000, type=TypeMouvement.ENTREE))
    repo.ajouter(Mouvement(date=date(2026, 6, 20), montant=100000, type=TypeMouvement.ENTREE))

    solde = calc.solde_periode(date(2026, 7, 1), date(2026, 7, 31))

    assert solde == 50000


def test_total_epargne_additionne_toutes_les_epargnes(calculateur):
    calc, repo = calculateur
    repo.ajouter(Mouvement(date=date(2026, 6, 1), montant=5000, type=TypeMouvement.EPARGNE))
    repo.ajouter(Mouvement(date=date(2026, 7, 1), montant=10000, type=TypeMouvement.EPARGNE))

    assert calc.total_epargne() == 15000


def test_repartition_categories_regroupe_par_categorie(calculateur):
    calc, repo = calculateur
    repo.ajouter(Mouvement(date=date(2026, 7, 5), montant=3000, type=TypeMouvement.DEPENSE, categorie="nourriture"))
    repo.ajouter(Mouvement(date=date(2026, 7, 10), montant=2000, type=TypeMouvement.DEPENSE, categorie="nourriture"))
    repo.ajouter(Mouvement(date=date(2026, 7, 12), montant=1500, type=TypeMouvement.DEPENSE, categorie="transport"))

    repartition = calc.repartition_categories(date(2026, 7, 1), date(2026, 7, 31))

    assert repartition == {"nourriture": 5000, "transport": 1500}