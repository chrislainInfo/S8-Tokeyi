"""
controllers.py — Orchestration entre app.py (Flask) et logic.py (métier).

*** NE PAS MODIFIER *** — ce fichier lit trajets.json et appelle les fonctions
que vous complétez dans logic.py.
"""
import json
import os
import logic
from werkzeug.security import generate_password_hash, check_password_hash

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "trajets.json")
COMPTES_PATH = os.path.join(os.path.dirname(__file__), "data", "comptes.json")


def _load():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _load_comptes():
    with open(COMPTES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_comptes(data):
    with open(COMPTES_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _enrichir_trajet(trajet, conducteurs, reservations):
    """Ajoute conducteur + places restantes réelles au trajet."""
    conducteur = next((c for c in conducteurs if c["id"] == trajet["conducteur_id"]), None)
    dispo = logic.verifier_place_disponible(trajet["id"], [trajet], reservations)
    return {
        **trajet,
        "conducteur": conducteur,
        "places_restantes": dispo["places_restantes"],
    }


def lister_trajets_disponibles(depart=None, arrivee=None):
    d = _load()
    trajets = logic.filtrer_trajets_disponibles(d["trajets"])
    if depart and arrivee:
        trajets = logic.filtrer_par_trajet_complet(trajets, depart, arrivee)
    elif depart:
        trajets = logic.filtrer_par_quartier_depart(trajets, depart)
    trajets = logic.trier_par_heure(trajets)
    return [_enrichir_trajet(t, d["conducteurs"], d["reservations"]) for t in trajets]


def get_trajet(trajet_id):
    d = _load()
    trajet = next((t for t in d["trajets"] if t["id"] == trajet_id), None)
    if trajet is None:
        return None
    return _enrichir_trajet(trajet, d["conducteurs"], d["reservations"])


def creer_reservation(trajet_id, passager_nom, passager_tel):
    d = _load()
    dispo = logic.verifier_place_disponible(trajet_id, d["trajets"], d["reservations"])
    if not dispo["place_dispo"]:
        return {"ok": False, "erreur": dispo["message"] or "Trajet indisponible"}
    nouvelle = {
        "id": max([r["id"] for r in d["reservations"]] + [0]) + 1,
        "trajet_id": trajet_id,
        "passager_nom": passager_nom,
        "passager_tel": passager_tel,
        "date_reservation": "2026-07-27",
        "statut": "en_attente",
    }
    d["reservations"].append(nouvelle)
    _save(d)
    return {"ok": True, "reservation": nouvelle}


def lister_reservations_passager(tel):
    d = _load()
    reservations = logic.historique_reservations_passager(tel, d["reservations"])
    result = []
    for r in reservations:
        trajet = next((t for t in d["trajets"] if t["id"] == r["trajet_id"]), None)
        if trajet:
            conducteur = next((c for c in d["conducteurs"] if c["id"] == trajet["conducteur_id"]), None)
            result.append({**r, "trajet": trajet, "conducteur": conducteur})
    return result


def get_dashboard():
    d = _load()
    indicateurs = logic.calculer_indicateurs_dashboard(
        d["trajets"], d["reservations"], d["conducteurs"]
    )
    top_conducteurs = logic.top_conducteurs_par_note(d["conducteurs"], n=3)
    trajet_top = logic.identifier_trajet_le_plus_reserve(d["trajets"], d["reservations"])
    trajets_par_quartier = logic.compter_trajets_par_quartier_depart(d["trajets"])
    prix_moyen_par_quartier = logic.calculer_prix_moyen_par_quartier(d["trajets"])
    taux_annulation = logic.calculer_taux_annulation(d["reservations"])
    return {
        **indicateurs,
        "top_conducteurs": top_conducteurs,
        "trajet_le_plus_reserve": trajet_top,
        "trajets_par_quartier": trajets_par_quartier,
        "prix_moyen_par_quartier": prix_moyen_par_quartier,
        "taux_annulation": taux_annulation,
    }


def lister_quartiers():
    return _load()["quartiers"]


def creer_compte(nom, telephone, mot_de_passe):
    d = _load_comptes()
    if not logic.verifier_telephone_disponible(d["comptes"], telephone):
        return {"ok": False, "erreur": "Ce numéro est déjà inscrit"}
    nouveau = {
        "id": max([c["id"] for c in d["comptes"]] + [0]) + 1,
        "nom": nom,
        "telephone": telephone,
        "mot_de_passe_hash": generate_password_hash(mot_de_passe),
    }
    d["comptes"].append(nouveau)
    _save_comptes(d)
    return {"ok": True, "compte": {"id": nouveau["id"], "nom": nom, "telephone": telephone}}


def login(telephone, mot_de_passe):
    d = _load_comptes()
    compte = logic.trouver_compte_par_telephone(d["comptes"], telephone)
    if compte is None or not check_password_hash(compte["mot_de_passe_hash"], mot_de_passe):
        return {"ok": False, "erreur": "Numéro ou mot de passe incorrect"}
    return {"ok": True, "compte": {"id": compte["id"], "nom": compte["nom"], "telephone": compte["telephone"]}}
