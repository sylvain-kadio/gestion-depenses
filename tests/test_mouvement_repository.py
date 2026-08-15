import pytest
from datetime import date

from src.database.connexion import initialiser_base
from src.repositories.mouvement_repository import MouvementRepository
from src.models.mouvement import Mouvement, TypeMouvement


@pytest.fixture
def repo(tmp_path):
    """Fournit un repository connecté à une base SQLite temporaire, neuve à chaque test."""
    chemin_base = tmp_path / "test.db"
    initialiser_base(chemin_base)
    return MouvementRepository(chemin_base)


def test_ajouter_attribue_un_id(repo):
    m = Mouvement(date=date.today(), montant=5000, type=TypeMouvement.ENTREE)
    m = repo.ajouter(m)
    assert m.id is not None


def test_lister_retourne_les_mouvements_ajoutes(repo):
    repo.ajouter(Mouvement(date=date.today(), montant=5000, type=TypeMouvement.ENTREE))
    repo.ajouter(Mouvement(date=date.today(), montant=1200, type=TypeMouvement.DEPENSE, categorie="transport"))

    mouvements = repo.lister()

    assert len(mouvements) == 2


def test_supprimer_retire_le_mouvement(repo):
    m = repo.ajouter(Mouvement(date=date.today(), montant=5000, type=TypeMouvement.ENTREE))

    repo.supprimer(m.id)

    assert repo.lister() == []

def test_modifier_met_a_jour_le_mouvement(repo):
    m = repo.ajouter(Mouvement(date=date.today(), montant=5000, type=TypeMouvement.ENTREE))

    m.montant = 8000
    m.note = "montant corrigé"
    repo.modifier(m)

    mouvements = repo.lister()
    assert len(mouvements) == 1
    assert mouvements[0].montant == 8000
    assert mouvements[0].note == "montant corrigé"