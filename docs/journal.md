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

## 31/07/2026 — 11h40 (suite 3) / 01/08/2026
- Écriture de l'interface CLI (main.py) : menu interactif avec boucle while
- Concepts découverts : input(), try/except pour la validation, dictionnaire d'actions, lambda, formatage f-string
- Test manuel complet du parcours utilisateur (entrée, dépense, épargne, consultation du solde)
- Solde vérifié : 2000 - 500 - 1000 = 500 FCFA, calcul correct
- Application fonctionnelle de bout en bout : modèle → base → services → interface

## 01/08/2026
- Amélioration UX : affichage automatique du solde du mois après chaque ajout (entrée, dépense, épargne)
- Correction d'une erreur d'indentation Python (unindent amount does not match)
- Application testée en conditions réelles avec de vraies données personnelles

## 01/08/2026 (suite)
- Ajout du filtre par période (jour/semaine/mois/année) dans le menu
- Nettoyage des saisies avec .strip() (espaces superflus dans catégorie/note)
- Ajout de modifier() au repository (UPDATE SQL paramétré)
- Ajout des options 9 (modifier) et 10 (supprimer) dans le menu
- À tester à la prochaine session : le parcours complet ajouter -> modifier -> supprimer

## 03/08/2026 — 22h01 (suite)
- Installation et configuration de Streamlit
- Création de app.py : sidebar (filtre période), indicateurs (solde, épargne), formulaire d'ajout, graphique de répartition, liste des mouvements
- Découverte du modèle de réexécution de Streamlit (script relancé à chaque interaction) et de st.form pour l'éviter
- Interface graphique testée et fonctionnelle, sans aucune modification des couches models/repositories/services
- Preuve concrète du bénéfice de l'architecture en couches : deux interfaces (CLI + Streamlit) partagent le même code métier

## 04/08/2026 — 00h00
- Interface Streamlit finalisée et testée (formulaire, indicateurs, graphique)
- Décision : le déploiement web Streamlit suffit pour un accès PC/Android/iOS via navigateur
- Projet natif Android/iOS mis de côté comme projet futur distinct, après finalisation de celui-ci
- Reste à faire : tests manquants, CI GitHub Actions, déploiement, README final

## 14/08/2026 — 23h33
- Ajout du test de modifier() dans test_mouvement_repository.py
- Ajout de tests_periode.py : jour, semaine, mois, annee (4 tests)
- Correction d'une erreur d'arborescence (dossier tests/tests/ en double)
- Total : 16 tests automatisés, tous passants

## 14/08/2026 — 23h33 (suite)
- Résolution du dossier tests/tests en double
- Ajout de 5 tests manquants (modifier + périodes), total 16 tests
- Mise en place de la CI GitHub Actions (tests + ruff), badge vert obtenu
- Correction des imports non triés (ruff --fix), configuration pyproject.toml (ignore DTZ011)
- Création du mode démo (variable d'environnement MODE_DEMO) pour protéger les vraies données personnelles
- Déploiement réussi sur Streamlit Community Cloud
- Application accessible publiquement via URL