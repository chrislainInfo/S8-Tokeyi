"""Tests pytest pour logic.py — Projet Covoiturage."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic import (
    filtrer_trajets_disponibles, filtrer_par_quartier_depart,
    filtrer_par_trajet_complet, trier_par_heure, trier_par_prix_croissant,
    compter_reservations_par_trajet, verifier_place_disponible,
    filtrer_reservations_par_statut, historique_reservations_passager,
    calculer_taux_annulation, compter_trajets_par_quartier_depart,
    top_conducteurs_par_note, calculer_prix_moyen_par_quartier,
    identifier_trajet_le_plus_reserve, calculer_indicateurs_dashboard,
    verifier_telephone_disponible, trouver_compte_par_telephone,
)

# === ZONE A ===

def test_filtrer_trajets_disponibles_normal():
    trajets = [{"id": 1, "places_dispo": 2}, {"id": 2, "places_dispo": 0}, {"id": 3, "places_dispo": 3}]
    assert filtrer_trajets_disponibles(trajets) == [{"id": 1, "places_dispo": 2}, {"id": 3, "places_dispo": 3}]

def test_filtrer_trajets_disponibles_vide():
    assert filtrer_trajets_disponibles([]) == []

def test_filtrer_trajets_disponibles_tous_complets():
    trajets = [{"id": 1, "places_dispo": 0}, {"id": 2, "places_dispo": 0}]
    assert filtrer_trajets_disponibles(trajets) == []

def test_filtrer_par_quartier_depart():
    trajets = [
        {"id": 1, "quartier_depart": "Bacongo"},
        {"id": 2, "quartier_depart": "Moungali"},
        {"id": 3, "quartier_depart": "Bacongo"},
    ]
    r = filtrer_par_quartier_depart(trajets, "Bacongo")
    assert len(r) == 2
    assert all(t["quartier_depart"] == "Bacongo" for t in r)

def test_filtrer_par_quartier_inexistant():
    trajets = [{"id": 1, "quartier_depart": "Bacongo"}]
    assert filtrer_par_quartier_depart(trajets, "Kintélé") == []

def test_filtrer_par_trajet_complet():
    trajets = [
        {"id": 1, "quartier_depart": "Bacongo", "quartier_arrivee": "Poto-Poto"},
        {"id": 2, "quartier_depart": "Bacongo", "quartier_arrivee": "Moungali"},
        {"id": 3, "quartier_depart": "Bacongo", "quartier_arrivee": "Poto-Poto"},
    ]
    r = filtrer_par_trajet_complet(trajets, "Bacongo", "Poto-Poto")
    assert len(r) == 2
    assert all(t["quartier_depart"] == "Bacongo" and t["quartier_arrivee"] == "Poto-Poto" for t in r)

def test_trier_par_heure():
    trajets = [{"id": 1, "heure": "08:00"}, {"id": 2, "heure": "07:00"}, {"id": 3, "heure": "07:30"}]
    r = trier_par_heure(trajets)
    assert [t["heure"] for t in r] == ["07:00", "07:30", "08:00"]

def test_trier_par_heure_ne_modifie_pas_original():
    trajets = [{"id": 1, "heure": "08:00"}, {"id": 2, "heure": "07:00"}]
    original = [dict(t) for t in trajets]
    trier_par_heure(trajets)
    assert trajets == original

def test_trier_par_prix_croissant():
    trajets = [{"id": 1, "prix_place": 700}, {"id": 2, "prix_place": 400}, {"id": 3, "prix_place": 500}]
    r = trier_par_prix_croissant(trajets)
    assert [t["prix_place"] for t in r] == [400, 500, 700]

# === ZONE B ===

def test_compter_reservations_par_trajet_normal():
    reservations = [
        {"trajet_id": 1, "statut": "effectue"},
        {"trajet_id": 1, "statut": "annule"},
        {"trajet_id": 1, "statut": "en_attente"},
        {"trajet_id": 2, "statut": "effectue"},
    ]
    assert compter_reservations_par_trajet(1, reservations) == 2

def test_compter_reservations_aucune():
    assert compter_reservations_par_trajet(99, []) == 0

def test_verifier_place_disponible_ok():
    trajets = [{"id": 1, "places_dispo": 3}]
    reservations = [{"trajet_id": 1, "statut": "effectue"}, {"trajet_id": 1, "statut": "en_attente"}]
    r = verifier_place_disponible(1, trajets, reservations)
    assert r["place_dispo"] is True
    assert r["places_restantes"] == 1

def test_verifier_place_disponible_complet():
    trajets = [{"id": 1, "places_dispo": 2}]
    reservations = [{"trajet_id": 1, "statut": "effectue"}, {"trajet_id": 1, "statut": "effectue"}]
    r = verifier_place_disponible(1, trajets, reservations)
    assert r["place_dispo"] is False
    assert r["places_restantes"] == 0
    assert "complet" in r["message"].lower()

def test_verifier_place_disponible_annulation_non_comptee():
    trajets = [{"id": 1, "places_dispo": 2}]
    reservations = [{"trajet_id": 1, "statut": "annule"}, {"trajet_id": 1, "statut": "annule"}]
    r = verifier_place_disponible(1, trajets, reservations)
    assert r["places_restantes"] == 2

def test_filtrer_reservations_par_statut():
    reservations = [
        {"id": 1, "statut": "effectue"},
        {"id": 2, "statut": "annule"},
        {"id": 3, "statut": "effectue"},
    ]
    r = filtrer_reservations_par_statut(reservations, "effectue")
    assert len(r) == 2

def test_historique_reservations_passager():
    reservations = [
        {"id": 1, "passager_tel": "066111"},
        {"id": 2, "passager_tel": "066222"},
        {"id": 3, "passager_tel": "066111"},
    ]
    r = historique_reservations_passager("066111", reservations)
    assert len(r) == 2

def test_calculer_taux_annulation_normal():
    reservations = [{"statut": "effectue"}, {"statut": "effectue"}, {"statut": "annule"}]
    assert calculer_taux_annulation(reservations) == 33.3

def test_calculer_taux_annulation_vide():
    assert calculer_taux_annulation([]) == 0.0

def test_calculer_taux_annulation_toutes_annulees():
    reservations = [{"statut": "annule"}, {"statut": "annule"}]
    assert calculer_taux_annulation(reservations) == 100.0

# === ZONE C ===

def test_compter_trajets_par_quartier_depart():
    trajets = [
        {"quartier_depart": "Bacongo"}, {"quartier_depart": "Bacongo"},
        {"quartier_depart": "Moungali"},
    ]
    r = compter_trajets_par_quartier_depart(trajets)
    assert r == {"Bacongo": 2, "Moungali": 1}

def test_compter_trajets_par_quartier_vide():
    assert compter_trajets_par_quartier_depart([]) == {}

def test_top_conducteurs_par_note():
    conducteurs = [
        {"nom": "A", "note": 4.5}, {"nom": "B", "note": 4.9}, {"nom": "C", "note": 4.7}
    ]
    r = top_conducteurs_par_note(conducteurs, n=2)
    assert len(r) == 2
    assert r[0]["nom"] == "B"
    assert r[1]["nom"] == "C"

def test_top_conducteurs_n_defaut():
    conducteurs = [{"nom": chr(65+i), "note": 4.0+i*0.1} for i in range(5)]
    r = top_conducteurs_par_note(conducteurs)
    assert len(r) == 3

def test_calculer_prix_moyen_par_quartier():
    trajets = [
        {"quartier_depart": "Bacongo", "prix_place": 500},
        {"quartier_depart": "Bacongo", "prix_place": 400},
        {"quartier_depart": "Bacongo", "prix_place": 600},
        {"quartier_depart": "Moungali", "prix_place": 700},
    ]
    r = calculer_prix_moyen_par_quartier(trajets)
    assert r["Bacongo"] == 500
    assert r["Moungali"] == 700

def test_identifier_trajet_le_plus_reserve():
    trajets = [
        {"id": 1, "quartier_depart": "Bacongo", "quartier_arrivee": "Poto-Poto"},
        {"id": 2, "quartier_depart": "Moungali", "quartier_arrivee": "Bacongo"},
    ]
    reservations = [
        {"trajet_id": 1, "statut": "effectue"},
        {"trajet_id": 1, "statut": "effectue"},
        {"trajet_id": 1, "statut": "effectue"},
        {"trajet_id": 2, "statut": "effectue"},
    ]
    r = identifier_trajet_le_plus_reserve(trajets, reservations)
    assert r["trajet_id"] == 1
    assert r["nombre_reservations"] == 3
    assert r["trajet_libelle"] == "Bacongo → Poto-Poto"

def test_identifier_trajet_aucune_reservation():
    trajets = [{"id": 1, "quartier_depart": "A", "quartier_arrivee": "B"}]
    assert identifier_trajet_le_plus_reserve(trajets, []) is None

def test_calculer_indicateurs_dashboard():
    trajets = [{"id": 1, "places_dispo": 3}, {"id": 2, "places_dispo": 0}, {"id": 3, "places_dispo": 2}]
    reservations = [{"statut": "effectue"}, {"statut": "en_attente"}, {"statut": "annule"}]
    conducteurs = [{"note": 4.5}, {"note": 4.9}, {"note": 4.7}]
    r = calculer_indicateurs_dashboard(trajets, reservations, conducteurs)
    assert r["total_trajets_disponibles"] == 2
    assert r["total_conducteurs_actifs"] == 3
    assert r["total_reservations_actives"] == 2
    assert r["note_moyenne_conducteurs"] == 4.7

def test_calculer_indicateurs_independance():
    """Cette fonction ne doit pas appeler d'autres fonctions de logic.py"""
    import logic
    import inspect
    src = inspect.getsource(logic.calculer_indicateurs_dashboard)
    # Vérifie qu'aucune autre fonction publique n'est appelée
    for fn in ["filtrer_trajets_disponibles", "compter_reservations_par_trajet",
               "top_conducteurs_par_note"]:
        assert fn + "(" not in src, f"calculer_indicateurs_dashboard ne doit pas appeler {fn}"

# === ZONE D ===

def test_verifier_telephone_disponible_pris():
    comptes = [{"id": 1, "telephone": "066123456"}]
    assert verifier_telephone_disponible(comptes, "066123456") is False

def test_verifier_telephone_disponible_libre():
    comptes = [{"id": 1, "telephone": "066123456"}]
    assert verifier_telephone_disponible(comptes, "055999999") is True

def test_verifier_telephone_disponible_liste_vide():
    assert verifier_telephone_disponible([], "066123456") is True

def test_trouver_compte_par_telephone_existant():
    comptes = [
        {"id": 1, "telephone": "066123456", "nom": "Franck"},
        {"id": 2, "telephone": "068234567", "nom": "Aurélie"},
    ]
    r = trouver_compte_par_telephone(comptes, "068234567")
    assert r["nom"] == "Aurélie"

def test_trouver_compte_par_telephone_absent():
    comptes = [{"id": 1, "telephone": "066123456", "nom": "Franck"}]
    assert trouver_compte_par_telephone(comptes, "055999999") is None
