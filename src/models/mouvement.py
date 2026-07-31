from dataclasses import dataclass
from datetime import date
from enum import Enum


class TypeMouvement(Enum):
    """Les trois natures possibles d'un mouvement d'argent."""
    ENTREE = "entree"
    DEPENSE = "depense"
    EPARGNE = "epargne"


@dataclass
class Mouvement:
    """Représente un mouvement d'argent unique : une entrée, une dépense ou une épargne."""

    date: date
    montant: float
    type: TypeMouvement
    categorie: str | None = None
    note: str | None = None
    id: int | None = None

    def __post_init__(self):
        if self.montant <= 0:
            raise ValueError("Le montant doit être strictement positif.")
        if self.type != TypeMouvement.DEPENSE and self.categorie is not None:
            raise ValueError("Seule une dépense peut avoir une catégorie.")