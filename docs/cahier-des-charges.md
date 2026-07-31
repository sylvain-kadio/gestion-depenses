1. Contexte et objectif

Application de suivi financier personnel adaptée à un revenu irrégulier (activité non fixe). L'objectif n'est pas de prévoir un budget, mais de suivre en temps réel le solde disponible entre les entrées d'argent et les dépenses, sur des périodes variables (jour, semaine, mois, année).

2. Utilisateur cible

Un seul utilisateur (toi), usage local, pas de compte ni d'authentification nécessaire dans la V1.

3. Fonctionnalités — méthode MoSCoW

Must have (indispensable pour la V1) :

Saisir une entrée d'argent (date, montant, note optionnelle)
Saisir une dépense (date, montant, catégorie libre optionnelle, note optionnelle)
Voir le solde du mois en cours par défaut, dès l'ouverture
Filtrer et recalculer le solde sur une période choisie (jour / semaine / mois / année / plage personnalisée)
Lister les mouvements d'une période, triés par date
Modifier ou supprimer un mouvement déjà saisi
- Enregistrer un mouvement d'épargne (montant, date, note optionnelle)
- Épargner un pourcentage d'une entrée d'argent au moment de sa saisie
- Voir le solde disponible = entrées − dépenses − épargne, sur la période choisie
- Voir le montant total épargné depuis le début (compteur global, indépendant de la période)

Should have (important, pas bloquant) :

Créer des catégories à la volée pendant la saisie d'une dépense
Voir une répartition des dépenses par catégorie sur une période
Export CSV des mouvements

Could have (si le temps le permet) :

Graphiques d'évolution du solde dans le temps
Comparaison entre deux périodes (ex. ce mois-ci vs le mois dernier)

Won't have (explicitement hors périmètre V1) :

Budget prévisionnel par catégorie
Comptes multiples ou multi-utilisateurs
Dépenses récurrentes automatiques
Synchronisation bancaire
4. Modèle de données
Mouvement
├── id (identifiant unique)
├── date
├── montant (positif, en FCFA ou devise choisie)
├── type : ENTREE | DEPENSE | EPARGNE
├── categorie (texte libre, optionnelle, uniquement si DEPENSE)
└── note (texte libre, optionnelle)

Une table de référence Categorie peut s'ajouter ensuite si tu veux éviter les doublons de saisie (ex. "nourriture" vs "Nourriture" vs "bouffe") — à voir en semaine 2 selon la complexité que tu veux gérer.

5. Règles de gestion
Un montant est toujours strictement positif ; le signe (+/−) est déterminé par le type
Le solde d'une période = somme des ENTREE − somme des DEPENSE sur cette période
Une dépense sans catégorie doit rester possible à tout moment (jamais de champ obligatoire bloquant)