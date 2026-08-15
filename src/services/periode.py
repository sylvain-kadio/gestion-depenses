import calendar
from datetime import date, timedelta
from enum import Enum


class TypePeriode(Enum):
    JOUR = "jour"
    SEMAINE = "semaine"
    MOIS = "mois"
    ANNEE = "annee"


def plage_periode(type_periode: TypePeriode, date_reference: date | None = None) -> tuple[date, date]:
    """Calcule la date de début et de fin d'une période, autour d'une date de référence (aujourd'hui par défaut)."""
    date_reference = date_reference or date.today()

    if type_periode == TypePeriode.JOUR:
        return date_reference, date_reference

    if type_periode == TypePeriode.SEMAINE:
        debut = date_reference - timedelta(days=date_reference.weekday())
        fin = debut + timedelta(days=6)
        return debut, fin

    if type_periode == TypePeriode.MOIS:
        debut = date_reference.replace(day=1)
        dernier_jour = calendar.monthrange(date_reference.year, date_reference.month)[1]
        fin = date_reference.replace(day=dernier_jour)
        return debut, fin

    if type_periode == TypePeriode.ANNEE:
        debut = date_reference.replace(month=1, day=1)
        fin = date_reference.replace(month=12, day=31)
        return debut, fin

    raise ValueError(f"Type de période inconnu : {type_periode}")