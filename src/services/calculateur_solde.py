from datetime import date

from src.models.mouvement import Mouvement, TypeMouvement
from src.repositories.mouvement_repository import MouvementRepository


class CalculateurSolde:
    """Calcule le solde disponible, l'épargne totale et la répartition des dépenses."""

    def __init__(self, repository: MouvementRepository):
        self.repository = repository

    def solde_periode(self, date_debut: date, date_fin: date) -> float:
        mouvements = self._mouvements_periode(date_debut, date_fin)
        entrees = sum(m.montant for m in mouvements if m.type == TypeMouvement.ENTREE)
        depenses = sum(m.montant for m in mouvements if m.type == TypeMouvement.DEPENSE)
        epargne = sum(m.montant for m in mouvements if m.type == TypeMouvement.EPARGNE)
        return entrees - depenses - epargne

    def total_epargne(self) -> float:
        mouvements = self.repository.lister()
        return sum(m.montant for m in mouvements if m.type == TypeMouvement.EPARGNE)

    def repartition_categories(self, date_debut: date, date_fin: date) -> dict[str, float]:
        mouvements = self._mouvements_periode(date_debut, date_fin)
        repartition: dict[str, float] = {}
        for m in mouvements:
            if m.type == TypeMouvement.DEPENSE and m.categorie:
                repartition[m.categorie] = repartition.get(m.categorie, 0) + m.montant
        return repartition

    def _mouvements_periode(self, date_debut: date, date_fin: date) -> list[Mouvement]:
        return [m for m in self.repository.lister() if date_debut <= m.date <= date_fin]