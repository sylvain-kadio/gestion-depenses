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
    print("8. Voir un résumé sur une période au choix (jour/semaine/mois/année)")
    print("9. Modifier un mouvement")
    print("10. Supprimer un mouvement")
    print("0. Quitter")


def demander_montant() -> float:
    while True:
        try:
            return float(input("Montant : "))
        except ValueError:
            print("Montant invalide, réessaie (ex: 5000 ou 1500.50).")


def choisir_type_periode() -> TypePeriode:
    print("Périodes disponibles : 1) Jour  2) Semaine  3) Mois  4) Année")
    correspondance = {
        "1": TypePeriode.JOUR,
        "2": TypePeriode.SEMAINE,
        "3": TypePeriode.MOIS,
        "4": TypePeriode.ANNEE,
    }
    while True:
        choix = input("Choix de la période : ")
        if choix in correspondance:
            return correspondance[choix]
        print("Choix invalide, réessaie.")


def ajouter_entree(repo: MouvementRepository, calculateur: CalculateurSolde) -> None:
    montant = demander_montant()
    note = input("Note (optionnel, Entrée pour passer) : ").strip() or None
    repo.ajouter(Mouvement(date=date.today(), montant=montant, type=TypeMouvement.ENTREE, note=note))
    print("Entrée enregistrée.")
    afficher_solde_mois(calculateur)


def ajouter_depense(repo: MouvementRepository, calculateur: CalculateurSolde) -> None:
    montant = demander_montant()
    categorie = input("Catégorie (optionnel, Entrée pour passer) : ").strip() or None
    note = input("Note (optionnel, Entrée pour passer) : ").strip() or None
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


def afficher_resume_periode(repo: MouvementRepository, calculateur: CalculateurSolde) -> None:
    type_periode = choisir_type_periode()
    debut, fin = plage_periode(type_periode)

    print(f"\nPériode : {debut} -> {fin}")

    solde = calculateur.solde_periode(debut, fin)
    print(f"Solde disponible : {solde} FCFA")

    repartition = calculateur.repartition_categories(debut, fin)
    if repartition:
        print("Répartition des dépenses :")
        for categorie, montant in repartition.items():
            print(f"  {categorie} : {montant} FCFA")

    mouvements = [m for m in repo.lister() if debut <= m.date <= fin]
    if mouvements:
        print("Mouvements de la période :")
        for m in mouvements:
            detail = f" ({m.categorie})" if m.categorie else ""
            note = f" - {m.note}" if m.note else ""
            print(f"  [{m.id}] {m.date} | {m.type.value:8} | {m.montant:>10.2f} FCFA{detail}{note}")
    else:
        print("Aucun mouvement sur cette période.")


def choisir_mouvement(repo: MouvementRepository) -> Mouvement | None:
    lister_mouvements(repo)
    mouvements = repo.lister()
    if not mouvements:
        return None
    try:
        id_choisi = int(input("ID du mouvement concerné : "))
    except ValueError:
        print("ID invalide.")
        return None
    mouvement = next((m for m in mouvements if m.id == id_choisi), None)
    if mouvement is None:
        print("Aucun mouvement avec cet ID.")
    return mouvement


def modifier_mouvement(repo: MouvementRepository, calculateur: CalculateurSolde) -> None:
    mouvement = choisir_mouvement(repo)
    if mouvement is None:
        return

    nouveau_montant = input(f"Nouveau montant (Entrée pour garder {mouvement.montant}) : ").strip()
    if nouveau_montant:
        try:
            mouvement.montant = float(nouveau_montant)
        except ValueError:
            print("Montant invalide, non modifié.")

    if mouvement.type == TypeMouvement.DEPENSE:
        nouvelle_categorie = input(f"Nouvelle catégorie (Entrée pour garder '{mouvement.categorie}') : ").strip()
        if nouvelle_categorie:
            mouvement.categorie = nouvelle_categorie

    nouvelle_note = input(f"Nouvelle note (Entrée pour garder '{mouvement.note}') : ").strip()
    if nouvelle_note:
        mouvement.note = nouvelle_note

    repo.modifier(mouvement)
    print("Mouvement modifié.")
    afficher_solde_mois(calculateur)


def supprimer_mouvement(repo: MouvementRepository, calculateur: CalculateurSolde) -> None:
    mouvement = choisir_mouvement(repo)
    if mouvement is None:
        return

    confirmation = input(f"Confirmer la suppression de [{mouvement.id}] {mouvement.montant} FCFA ? (o/n) : ").strip().lower()
    if confirmation == "o":
        repo.supprimer(mouvement.id)
        print("Mouvement supprimé.")
        afficher_solde_mois(calculateur)
    else:
        print("Suppression annulée.")


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
        "8": lambda: afficher_resume_periode(repo, calculateur),
        "9": lambda: modifier_mouvement(repo, calculateur),
        "10": lambda: supprimer_mouvement(repo, calculateur),
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