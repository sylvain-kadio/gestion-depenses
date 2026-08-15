# Pitch d'entretien — Gestion de Dépenses

## Pitch en 2 minutes

"J'ai développé une application de gestion de dépenses en Python, mais pas
comme un exercice de tutoriel : je l'ai conçue pour mon propre usage réel,
avec un revenu irrégulier d'indépendant. Les applications de budget classiques
supposent un salaire fixe mensuel — ça ne correspondait pas à ma situation.

J'ai suivi une vraie démarche projet : cahier des charges, user stories,
modélisation UML, avant d'écrire la moindre ligne de code. L'architecture
est en couches strictes — modèle, repository, services, interface — ce qui
m'a permis d'ajouter une interface web Streamlit en plus de la version ligne
de commande, sans toucher à la logique métier.

Le projet est testé automatiquement — 16 tests avec pytest — et une CI
GitHub Actions vérifie chaque push. Il est déployé publiquement sur Streamlit
Cloud, avec une version démo à données fictives pour protéger mes vraies
données financières.

Tout le code est sur GitHub, avec un historique de commits et un journal de
bord qui documente chaque décision technique prise."

## Questions probables et pistes de réponse

**Pourquoi SQLite plutôt que PostgreSQL/MySQL ?**
Application locale, mono-utilisateur. SQLite ne demande aucune installation
de serveur, stocke tout dans un seul fichier. PostgreSQL aurait été de la
sur-ingénierie pour ce besoin — mais je sais identifier le seuil où il
faudrait migrer (multi-utilisateur, accès concurrent).

**Comment ferais-tu évoluer l'app pour plusieurs utilisateurs ?**
Ajouter une table Utilisateur, une authentification, filtrer chaque requête
par utilisateur connecté, et à ce moment-là migrer vers PostgreSQL pour gérer
les accès concurrents correctement.

**Parle-moi d'un bug ou d'une difficulté rencontrée.**
(Piocher dans docs/journal.md — exemples réels : l'erreur d'indentation
Python, le dossier tests/tests dupliqué par erreur, la gestion de
l'exécution PowerShell bloquée par défaut sur Windows.)

**Comment as-tu utilisé l'IA sur ce projet ?**
Comme assistant pédagogique et outil de productivité, jamais comme
générateur de code que je ne comprends pas. Chaque concept (dataclass, enum,
requêtes paramétrées, fixtures pytest) m'a été expliqué avant d'être utilisé.
Je peux expliquer et modifier n'importe quelle ligne du projet.

**Pourquoi une architecture en couches, pour un projet aussi petit ?**
Preuve concrète : j'ai ajouté Streamlit sans modifier models/, repositories/
ou services/. Si demain je change de base de données, seul repositories/
change. C'est un investissement qui se rembourse dès qu'un projet dépasse
le stade du script isolé.

**Qu'est-ce que tu referais différemment ?**
(Réponse honnête à préparer soi-même — montre du recul, pas juste de
l'exécution.)

## Points forts à mettre en avant spontanément

- Démarche projet complète, pas juste du code : analyse, UML, architecture
- Tests automatisés + CI, pas juste "ça marche sur ma machine"
- Réflexion sur la confidentialité des données au moment du déploiement
  (mode démo vs données réelles) — signal de maturité, pas juste de
  compétence technique
- Deux interfaces sur la même logique métier, preuve du découplage
- Journal de bord démontrant une vraie progression datée, pas un projet
  bâclé en un week-end