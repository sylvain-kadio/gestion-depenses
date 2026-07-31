import sqlite3
from pathlib import Path

CHEMIN_BASE = Path(__file__).parent.parent.parent / "depenses.db"
CHEMIN_SCHEMA = Path(__file__).parent / "schema.sql"


def obtenir_connexion(chemin_base: Path = CHEMIN_BASE) -> sqlite3.Connection:
    """Ouvre une connexion à la base SQLite. Un autre chemin peut être fourni pour les tests."""
    connexion = sqlite3.connect(chemin_base)
    connexion.row_factory = sqlite3.Row
    return connexion


def initialiser_base(chemin_base: Path = CHEMIN_BASE) -> None:
    """Crée la table mouvements si elle n'existe pas encore."""
    with obtenir_connexion(chemin_base) as connexion:
        script = CHEMIN_SCHEMA.read_text(encoding="utf-8")
        connexion.executescript(script)