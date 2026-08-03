import streamlit as st
from datetime import date

from src.database.connexion import initialiser_base
from src.models.mouvement import Mouvement, TypeMouvement
from src.repositories.mouvement_repository import MouvementRepository
from src.services.calculateur_solde import CalculateurSolde
from src.services.periode import TypePeriode, plage_periode

st.set_page_config(page_title="Gestion de dépenses", page_icon="💰")

initialiser_base()
repo = MouvementRepository()
calculateur = CalculateurSolde(repo)

st.title("💰 Gestion de dépenses")

# --- Sidebar : choix de la période ---
st.sidebar.header("Période")
label_periode = st.sidebar.selectbox("Afficher", ["Mois", "Jour", "Semaine", "Année"])
correspondance = {
    "Jour": TypePeriode.JOUR,
    "Semaine": TypePeriode.SEMAINE,
    "Mois": TypePeriode.MOIS,
    "Année": TypePeriode.ANNEE,
}
debut, fin = plage_periode(correspondance[label_periode])
st.sidebar.caption(f"{debut} → {fin}")

# --- Indicateurs principaux ---
solde = calculateur.solde_periode(debut, fin)
epargne_totale = calculateur.total_epargne()

col1, col2 = st.columns(2)
col1.metric("Solde disponible", f"{solde:.0f} FCFA")
col2.metric("Épargne totale", f"{epargne_totale:.0f} FCFA")

st.divider()

# --- Formulaire d'ajout ---
st.subheader("Ajouter un mouvement")

with st.form("ajout_mouvement", clear_on_submit=True):
    type_choisi = st.radio("Type", ["Entrée", "Dépense", "Épargne"], horizontal=True)
    montant = st.number_input("Montant (FCFA)", min_value=0.0, step=100.0)

    categorie = ""
    if type_choisi == "Dépense":
        categorie = st.text_input("Catégorie (optionnel)")

    note = st.text_input("Note (optionnel)")
    valider = st.form_submit_button("Enregistrer")

    if valider:
        if montant <= 0:
            st.error("Le montant doit être positif.")
        else:
            type_mouvement = {
                "Entrée": TypeMouvement.ENTREE,
                "Dépense": TypeMouvement.DEPENSE,
                "Épargne": TypeMouvement.EPARGNE,
            }[type_choisi]
            repo.ajouter(Mouvement(
                date=date.today(),
                montant=montant,
                type=type_mouvement,
                categorie=categorie.strip() or None,
                note=note.strip() or None,
            ))
            st.success("Mouvement enregistré.")
            st.rerun()

st.divider()

# --- Répartition des dépenses ---
st.subheader("Répartition des dépenses")
repartition = calculateur.repartition_categories(debut, fin)
if repartition:
    st.bar_chart(repartition)
else:
    st.info("Aucune dépense catégorisée sur cette période.")

st.divider()

# --- Liste des mouvements ---
st.subheader("Mouvements de la période")
mouvements = [m for m in repo.lister() if debut <= m.date <= fin]

if mouvements:
    for m in reversed(mouvements):
        detail = f" · {m.categorie}" if m.categorie else ""
        note_txt = f" — {m.note}" if m.note else ""
        signe = "+" if m.type == TypeMouvement.ENTREE else "-"
        st.write(f"`{m.date}` **{signe}{m.montant:.0f} FCFA** [{m.type.value}]{detail}{note_txt}")
else:
    st.info("Aucun mouvement sur cette période.")