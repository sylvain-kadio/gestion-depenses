from datetime import date

import pytest

from src.models.mouvement import Mouvement, TypeMouvement


def test_creation_mouvement_valide():
    m = Mouvement(date=date.today(), montant=5000, type=TypeMouvement.ENTREE)
    assert m.montant == 5000
    assert m.type == TypeMouvement.ENTREE


def test_montant_negatif_refuse():
    with pytest.raises(ValueError):
        Mouvement(date=date.today(), montant=-5000, type=TypeMouvement.ENTREE)


def test_entree_avec_categorie_refusee():
    with pytest.raises(ValueError):
        Mouvement(date=date.today(), montant=1000, type=TypeMouvement.ENTREE, categorie="loyer")


def test_depense_avec_categorie_acceptee():
    m = Mouvement(date=date.today(), montant=1500, type=TypeMouvement.DEPENSE, categorie="nourriture")
    assert m.categorie == "nourriture"