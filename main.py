from datetime import date

from src.database.connexion import initialiser_base
from src.models.mouvement import Mouvement, TypeMouvement
from src.repositories.mouvement_repository import MouvementRepository
from src.services.calculateur_solde import CalculateurSolde
from src.services.periode import TypePeriode, plage_periode


def afficher_menu() -> None:
    print("\n--- Gestion de dépenses ---")
    print("1. Ajouter une entrée d'argent")
    print("2. Ajouter une dépense")
    print("3. Ajouter une épargne")
    print("4. Voir le solde du mois")
    print("5. Voir l'épargne totale")
    print("6. Voir la répartition des dépenses du mois")
    print("7. Lister tous les mouvements")
    print("0. Quitter")


def demander_montant() -> float:
    while True:
        try:
            return float(input("Montant : "))
        except ValueError:
            print("Montant invalide, réessaie (ex: 5000 ou 1500.50).")


def ajouter_entree(repo: MouvementRepository, calculateur: CalculateurSolde) -> None:
    montant = demander_montant()
    note = input("Note (optionnel, Entrée pour passer) : ") or None
    repo.ajouter(Mouvement(date=date.today(), montant=montant, type=TypeMouvement.ENTREE, note=note))
    print("Entrée enregistrée.")
    afficher_solde_mois(calculateur)


def ajouter_depense(repo: MouvementRepository, calculateur: CalculateurSolde) -> None:
    montant = demander_montant()
    categorie = input("Catégorie (optionnel, Entrée pour passer) : ") or None
    note = input("Note (optionnel, Entrée pour passer) : ") or None
    repo.ajouter(Mouvement(date=date.today(), montant=montant, type=TypeMouvement.DEPENSE, categorie=categorie, note=note))
    print("Dépense enregistrée.")
    afficher_solde_mois(calculateur)


def ajouter_epargne(repo: MouvementRepository, calculateur: CalculateurSolde) -> None:
    montant = demander_montant()
    repo.ajouter(Mouvement(date=date.today(), montant=montant, type=TypeMouvement.EPARGNE))
    print("Épargne enregistrée.")
    afficher_solde_mois(calculateur)


def afficher_solde_mois(calculateur: CalculateurSolde) -> None:
    debut, fin = plage_periode(TypePeriode.MOIS)
    solde = calculateur.solde_periode(debut, fin)
    print(f"Solde disponible du mois ({debut} -> {fin}) : {solde} FCFA")


def afficher_epargne_totale(calculateur: CalculateurSolde) -> None:
    print(f"Épargne totale accumulée : {calculateur.total_epargne()} FCFA")


def afficher_repartition(calculateur: CalculateurSolde) -> None:
    debut, fin = plage_periode(TypePeriode.MOIS)
    repartition = calculateur.repartition_categories(debut, fin)
    if not repartition:
        print("Aucune dépense catégorisée ce mois-ci.")
        return
    print(f"Répartition des dépenses du mois ({debut} -> {fin}) :")
    for categorie, montant in repartition.items():
        print(f"  {categorie} : {montant} FCFA")


def lister_mouvements(repo: MouvementRepository) -> None:
    mouvements = repo.lister()
    if not mouvements:
        print("Aucun mouvement enregistré.")
        return
    for m in mouvements:
        detail = f" ({m.categorie})" if m.categorie else ""
        note = f" - {m.note}" if m.note else ""
        print(f"[{m.id}] {m.date} | {m.type.value:8} | {m.montant:>10.2f} FCFA{detail}{note}")


def main() -> None:
    initialiser_base()
    repo = MouvementRepository()
    calculateur = CalculateurSolde(repo)

    actions = {
        "1": lambda: ajouter_entree(repo, calculateur),
        "2": lambda: ajouter_depense(repo, calculateur),
        "3": lambda: ajouter_epargne(repo, calculateur),
        "4": lambda: afficher_solde_mois(calculateur),
        "5": lambda: afficher_epargne_totale(calculateur),
        "6": lambda: afficher_repartition(calculateur),
        "7": lambda: lister_mouvements(repo),
    }

    while True:
        afficher_menu()
        choix = input("Choix : ")
        if choix == "0":
            print("À bientôt.")
            break
        action = actions.get(choix)
        if action:
            action()
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()