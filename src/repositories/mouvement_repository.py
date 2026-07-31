from datetime import date
from pathlib import Path
import sqlite3

from src.models.mouvement import Mouvement, TypeMouvement
from src.database.connexion import obtenir_connexion, CHEMIN_BASE


class MouvementRepository:
    """Gère la persistance des mouvements en base SQLite."""

    def __init__(self, chemin_base: Path = CHEMIN_BASE):
        self.chemin_base = chemin_base

    def ajouter(self, mouvement: Mouvement) -> Mouvement:
        with obtenir_connexion(self.chemin_base) as connexion:
            curseur = connexion.execute(
                """
                INSERT INTO mouvements (date, montant, type, categorie, note)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    mouvement.date.isoformat(),
                    mouvement.montant,
                    mouvement.type.value,
                    mouvement.categorie,
                    mouvement.note,
                ),
            )
            mouvement.id = curseur.lastrowid
        return mouvement

    def lister(self) -> list[Mouvement]:
        with obtenir_connexion(self.chemin_base) as connexion:
            lignes = connexion.execute("SELECT * FROM mouvements ORDER BY date").fetchall()
        return [self._vers_mouvement(ligne) for ligne in lignes]

    def supprimer(self, id_mouvement: int) -> None:
        with obtenir_connexion(self.chemin_base) as connexion:
            connexion.execute("DELETE FROM mouvements WHERE id = ?", (id_mouvement,))

    def _vers_mouvement(self, ligne: sqlite3.Row) -> Mouvement:
        return Mouvement(
            id=ligne["id"],
            date=date.fromisoformat(ligne["date"]),
            montant=ligne["montant"],
            type=TypeMouvement(ligne["type"]),
            categorie=ligne["categorie"],
            note=ligne["note"],
        )