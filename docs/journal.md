# Journal de bord

## 23/07/2026
- Installation de l'environnement complet : Python, VS Code, Git
- Création du compte GitHub, configuration de l'identité Git
- Initialisation du dépôt, premier commit
- Rédaction du cahier des charges et des user stories
- Diagrammes UML (classes, cas d'utilisation)
- Mise en place de l'architecture en couches (models, repositories, services, database, tests)
- Écriture de la classe `Mouvement` avec validation métier

## 31/07/2026 — 01:00
- (à compléter en fin de session)

## 31/07/2026 — 11h40
- Test manuel de la classe Mouvement dans l'interpréteur (validation des règles de gestion)
- Écriture de 4 tests unitaires avec pytest
- Tous les tests passent (4 passed)
- Découverte de Ruff comme aide au style de code (DTZ011)

## 31/07/2026 — 11h40 (suite)
- Création du schéma SQLite et du module de connexion
- Repository MouvementRepository : ajouter, lister, supprimer
- Test manuel en conditions réelles (persistance vérifiée dans depenses.db)
- Refactoring pour rendre le repository testable (chemin de base injectable)
- 3 tests du repository avec fixture pytest et base temporaire (tmp_path)
- Total : 7 tests, tous passants

## 31/07/2026 — 11h40 (suite 2)
- Services : gestion des périodes (jour/semaine/mois/année) et calculateur de solde
- Règle métier appliquée : solde = entrées - dépenses - épargne
- Tests manuels en conditions réelles (calcul vérifié à la main : 50000 - 5000 - 10000 = 35000)
- 4 tests du calculateur : solde par période, exclusion hors plage, épargne totale, répartition par catégorie
- Total : 11 tests, tous passants