from datetime import date

from src.services.periode import TypePeriode, plage_periode


def test_periode_jour_retourne_la_meme_date():
    debut, fin = plage_periode(TypePeriode.JOUR, date(2026, 8, 14))
    assert debut == date(2026, 8, 14)
    assert fin == date(2026, 8, 14)


def test_periode_semaine_commence_un_lundi():
    debut, fin = plage_periode(TypePeriode.SEMAINE, date(2026, 8, 14))
    assert debut.weekday() == 0
    assert fin.weekday() == 6
    assert (fin - debut).days == 6


def test_periode_mois_couvre_le_mois_entier():
    debut, fin = plage_periode(TypePeriode.MOIS, date(2026, 8, 14))
    assert debut == date(2026, 8, 1)
    assert fin == date(2026, 8, 31)


def test_periode_annee_couvre_l_annee_entiere():
    debut, fin = plage_periode(TypePeriode.ANNEE, date(2026, 8, 14))
    assert debut == date(2026, 1, 1)
    assert fin == date(2026, 12, 31)