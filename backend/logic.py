"""
========================================================================
  LOGIC.PY  —  À COMPLÉTER PAR L'ÉQUIPE DATA SCIENCE
========================================================================
BraCovoit — Covoiturage inter-quartiers, Brazzaville

Vous n'écrivez QUE des fonctions (ce que vous savez déjà faire : boucles,
conditions, dictionnaires). Vous ne touchez à AUCUN autre fichier.

Chaque fonction reçoit des données simples (listes, dictionnaires) et doit
RENVOYER un résultat. Pas de print, pas de input, pas de requête réseau,
pas de Flask, pas de base de données. Juste : des paramètres entrent, une
valeur sort.

La toute première fonction du fichier (filtrer_trajets_disponibles) est
déjà entièrement résolue, avec des commentaires qui expliquent chaque
étape. Regardez-la avant de commencer : elle montre le style de code et
le niveau de détail attendus. Toutes les autres fonctions sont à
compléter (repérez les `# TODO : à compléter` suivis de `pass`).

Le fichier est découpé en 4 zones de responsabilité. Répartissez-vous les
zones selon le nombre de personnes dans l'équipe.

  - ZONE A : Recherche & disponibilité      — 5 fonctions
  - ZONE B : Réservations & suivi           — 5 fonctions
  - ZONE C : Statistiques & tableau de bord — 5 fonctions
  - ZONE D : Comptes & authentification     — 2 fonctions

Quand vos fonctions sont correctes :
  1. les tests passent au vert   (python -m pytest -v, depuis backend/)
  2. l'API démarre et renvoie les bons résultats  (python app.py)

Remplacez chaque `pass` / `# TODO` par votre code.
========================================================================
"""


# ========================================================================
# ZONE A — Recherche & disponibilité
# ========================================================================

def filtrer_trajets_disponibles(trajets):
    """
    Retourne uniquement les trajets qui ont encore au moins 1 place
    disponible (places_dispo >= 1). Utilisée en tout premier dans le
    pipeline de recherche, pour ne jamais montrer un trajet déjà complet.

    Paramètre :
        trajets : liste de dict, chacun avec au minimum une clé
                  "places_dispo" (int)

    Retourne :
        une liste de trajets (dict), dans le même ordre, en ne gardant que
        ceux dont places_dispo est supérieur ou égal à 1.

    Exemple :
        entrée -> [{"id": 1, "places_dispo": 2}, {"id": 2, "places_dispo": 0},
                   {"id": 3, "places_dispo": 3}]
        sortie -> [{"id": 1, "places_dispo": 2}, {"id": 3, "places_dispo": 3}]
    """
    # On construit une nouvelle liste, vide au départ.
    # TODO : à compléter
    pass


def filtrer_par_quartier_depart(trajets, quartier):
    """
    Retourne les trajets qui partent du quartier donné. Utilisée quand un
    passager choisit un quartier de départ dans le filtre de recherche.

    Paramètres :
        trajets  : liste de dict, chacun avec une clé "quartier_depart" (str)
        quartier : nom du quartier recherché (str), ex. "Bacongo"

    Retourne :
        une liste de trajets (dict) dont "quartier_depart" est exactement
        égal à quartier (comparaison stricte, respecter la casse).

    Exemple :
        trajets = [
            {"id": 1, "quartier_depart": "Bacongo"},
            {"id": 2, "quartier_depart": "Moungali"},
            {"id": 3, "quartier_depart": "Bacongo"},
        ]
        filtrer_par_quartier_depart(trajets, "Bacongo")
        -> [{"id": 1, "quartier_depart": "Bacongo"}, {"id": 3, "quartier_depart": "Bacongo"}]
    """
    # TODO : à compléter
    pass


def filtrer_par_trajet_complet(trajets, depart, arrivee):
    """
    Retourne les trajets qui vont précisément de "depart" à "arrivee".
    Utilisée quand un passager recherche un trajet précis (les deux
    quartiers renseignés), par exemple "Bacongo → Poto-Poto".

    Paramètres :
        trajets : liste de dict trajet
        depart  : quartier de départ recherché (str)
        arrivee : quartier d'arrivée recherché (str)

    Retourne :
        une liste de trajets dont quartier_depart == depart ET
        quartier_arrivee == arrivee (les deux conditions à la fois).

    Exemple :
        trajets = [
            {"id": 1, "quartier_depart": "Bacongo", "quartier_arrivee": "Poto-Poto"},
            {"id": 2, "quartier_depart": "Bacongo", "quartier_arrivee": "Moungali"},
        ]
        filtrer_par_trajet_complet(trajets, "Bacongo", "Poto-Poto")
        -> [{"id": 1, "quartier_depart": "Bacongo", "quartier_arrivee": "Poto-Poto"}]
    """
    # TODO : à compléter
    pass


def trier_par_heure(trajets):
    """
    Trie les trajets par heure croissante (du plus tôt le matin au plus
    tard). Utilisée pour que les résultats de recherche s'affichent dans
    l'ordre chronologique de la journée.

    Paramètre :
        trajets : liste de dict, chacun avec une clé "heure" au format
                  texte "HH:MM" (ex. "07:30")

    Retourne :
        une NOUVELLE liste de trajets, triée par heure croissante. Ne
        modifie PAS la liste reçue en paramètre (indice : la fonction
        native sorted() ne modifie jamais la liste d'origine, contrairement
        à .sort()).

    Exemple :
        entrée -> [{"heure": "08:00"}, {"heure": "07:00"}, {"heure": "07:30"}]
        sortie -> [{"heure": "07:00"}, {"heure": "07:30"}, {"heure": "08:00"}]

        Astuce : comparer des heures au format "HH:MM" comme du texte
        fonctionne directement ("07:00" < "07:30" < "08:00" est vrai en
        comparaison de chaînes), pas besoin de les convertir en nombres.
    """
    # TODO : à compléter
    pass


def trier_par_prix_croissant(trajets):
    """
    Trie les trajets par prix croissant (du moins cher au plus cher).
    Utilisée pour l'option de tri "prix" côté recherche.

    Paramètre :
        trajets : liste de dict, chacun avec une clé "prix_place" (int, en FCFA)

    Retourne :
        une NOUVELLE liste de trajets, triée par prix_place croissant.

    Exemple :
        entrée -> [{"prix_place": 700}, {"prix_place": 400}, {"prix_place": 500}]
        sortie -> [{"prix_place": 400}, {"prix_place": 500}, {"prix_place": 700}]
    """
    # TODO : à compléter
    pass


# ========================================================================
# ZONE B — Réservations & suivi
# ========================================================================

def compter_reservations_par_trajet(trajet_id, reservations):
    """
    Compte le nombre de réservations actives (statut "effectue" OU
    "en_attente") pour un trajet donné. Les réservations "annule" ne
    comptent PAS, puisqu'elles libèrent la place.

    Paramètres :
        trajet_id    : identifiant du trajet recherché (int)
        reservations : liste de dict, chacun avec les clés "trajet_id" (int)
                       et "statut" (str, l'une de "effectue"/"en_attente"/"annule")

    Retourne :
        un entier : le nombre de réservations non annulées pour ce trajet.

    Exemple :
        trajet_id = 1
        reservations = [
            {"trajet_id": 1, "statut": "effectue"},
            {"trajet_id": 1, "statut": "annule"},
            {"trajet_id": 1, "statut": "en_attente"},
            {"trajet_id": 2, "statut": "effectue"},
        ]
        compter_reservations_par_trajet(1, reservations) -> 2
        (les 2 réservations du trajet 1 qui ne sont pas "annule";
        la réservation du trajet 2 ne compte pas, ce n'est pas le bon trajet)
    """
    # TODO : à compléter
    pass


def verifier_place_disponible(trajet_id, trajets, reservations):
    """
    Vérifie s'il reste au moins une place libre sur un trajet, en tenant
    compte des réservations déjà enregistrées. C'est LA fonction qui
    protège contre la surréservation — utilisée par controllers.py à
    chaque tentative de réservation, avant de l'accepter.

    Règle métier : places_restantes = places_dispo - réservations actives.
    S'il reste au moins 1 place, la réservation peut être acceptée.

    Paramètres :
        trajet_id    : identifiant du trajet concerné (int)
        trajets      : liste de dict trajet, chacun avec "id" (int) et
                       "places_dispo" (int)
        reservations : liste de dict réservation, chacun avec "trajet_id"
                       (int) et "statut" (str)

    Retourne :
        un dictionnaire avec EXACTEMENT ces 3 clés :
        {
            "place_dispo": bool,       # True s'il reste au moins 1 place
            "places_restantes": int,   # 0 si complet ou trajet introuvable
            "message": str             # message d'erreur, "" si tout va bien
        }

        Si le trajet_id n'existe pas dans trajets, retourner :
        {"place_dispo": False, "places_restantes": 0, "message": "Trajet introuvable"}

        Si le trajet existe mais n'a plus de place, retourner :
        {"place_dispo": False, "places_restantes": 0, "message": "Trajet complet"}

    Exemple :
        trajets = [{"id": 1, "places_dispo": 3}]
        reservations = [
            {"trajet_id": 1, "statut": "effectue"},
            {"trajet_id": 1, "statut": "en_attente"},
        ]
        verifier_place_disponible(1, trajets, reservations)
        -> {"place_dispo": True, "places_restantes": 1, "message": ""}
        (3 places au total, 2 déjà prises par des réservations actives,
        il en reste 1)
    """
    # TODO : à compléter
    pass


def filtrer_reservations_par_statut(reservations, statut):
    """
    Retourne les réservations correspondant exactement au statut donné.
    Utilisée sur la page "Mes trajets" quand le passager filtre son
    historique (par exemple pour ne voir que ses trajets "effectue").

    Paramètres :
        reservations : liste de dict réservation, chacun avec "statut" (str)
        statut       : la valeur recherchée, l'une de "effectue",
                       "en_attente" ou "annule"

    Retourne :
        une liste de réservations dont "statut" == statut.

    Exemple :
        reservations = [
            {"id": 1, "statut": "effectue"},
            {"id": 2, "statut": "annule"},
            {"id": 3, "statut": "effectue"},
        ]
        filtrer_reservations_par_statut(reservations, "effectue")
        -> [{"id": 1, "statut": "effectue"}, {"id": 3, "statut": "effectue"}]
    """
    # TODO : à compléter
    pass


def historique_reservations_passager(passager_tel, reservations):
    """
    Retourne toutes les réservations faites par un passager, identifié
    par son numéro de téléphone. Utilisée sur la page "Mes trajets" pour
    afficher l'historique complet d'un passager.

    Paramètres :
        passager_tel : numéro de téléphone du passager (str), ex. "067111222"
        reservations : liste de dict, chacun avec une clé "passager_tel" (str)

    Retourne :
        une liste de réservations dont "passager_tel" correspond exactement
        au numéro donné.

    Exemple :
        reservations = [
            {"id": 1, "passager_tel": "067111222"},
            {"id": 2, "passager_tel": "068222333"},
            {"id": 3, "passager_tel": "067111222"},
        ]
        historique_reservations_passager("067111222", reservations)
        -> [{"id": 1, "passager_tel": "067111222"}, {"id": 3, "passager_tel": "067111222"}]
    """
    # TODO : à compléter
    pass


def calculer_taux_annulation(reservations):
    """
    Calcule le pourcentage de réservations annulées sur l'ensemble des
    réservations. Utilisée pour l'indicateur de fiabilité du service
    affiché sur le tableau de bord.

    Formule : (nombre de réservations "annule" / nombre total) * 100

    Paramètre :
        reservations : liste de dict, chacun avec une clé "statut" (str)

    Retourne :
        un nombre à virgule (float), arrondi à 1 décimale, représentant
        le pourcentage. Si la liste est vide, retourner 0.0 (pour éviter
        une division par zéro).

    Exemple :
        reservations = [
            {"statut": "effectue"}, {"statut": "effectue"}, {"statut": "annule"}
        ]
        calculer_taux_annulation(reservations) -> 33.3
        (1 annulée sur 3 réservations, soit 33.33...%, arrondi à 33.3)
    """
    # TODO : à compléter
    pass


# ========================================================================
# ZONE C — Statistiques & tableau de bord
# ========================================================================

def compter_trajets_par_quartier_depart(trajets):
    """
    Compte combien de trajets partent de chaque quartier. Utilisée pour
    le tableau "Répartition par quartier" du tableau de bord.

    Paramètre :
        trajets : liste de dict, chacun avec une clé "quartier_depart" (str)

    Retourne :
        un dictionnaire {quartier: nombre_de_trajets}, avec une clé par
        quartier distinct présent dans la liste reçue.

    Exemple :
        trajets = [
            {"quartier_depart": "Bacongo"}, {"quartier_depart": "Bacongo"},
            {"quartier_depart": "Moungali"},
        ]
        compter_trajets_par_quartier_depart(trajets)
        -> {"Bacongo": 2, "Moungali": 1}
    """
    # TODO : à compléter
    pass


def top_conducteurs_par_note(conducteurs, n=3):
    """
    Retourne les n conducteurs les mieux notés, du meilleur au moins bon.
    Utilisée pour le classement "Top 3 conducteurs" du tableau de bord.

    Paramètres :
        conducteurs : liste de dict, chacun avec une clé "note" (float,
                      entre 0 et 5)
        n           : nombre de conducteurs à retourner (int, 3 par défaut)

    Retourne :
        une liste des n conducteurs (dict complets, avec toutes leurs clés
        d'origine) ayant les notes les plus élevées, triée par note
        décroissante. Si moins de n conducteurs existent, retourner tous
        ceux qui existent.

    Exemple :
        conducteurs = [
            {"nom": "Franck", "note": 4.5},
            {"nom": "Jean", "note": 4.9},
            {"nom": "Sandra", "note": 4.7},
        ]
        top_conducteurs_par_note(conducteurs, n=2)
        -> [{"nom": "Jean", "note": 4.9}, {"nom": "Sandra", "note": 4.7}]
    """
    # TODO : à compléter
    pass


def calculer_prix_moyen_par_quartier(trajets):
    """
    Calcule le prix moyen des trajets partant de chaque quartier. Utilisée
    dans le tableau du dashboard, à côté du nombre de trajets par quartier.

    Paramètre :
        trajets : liste de dict, chacun avec les clés "quartier_depart"
                  (str) et "prix_place" (int, en FCFA)

    Retourne :
        un dictionnaire {quartier: prix_moyen}, où prix_moyen est un
        entier arrondi (utilisez round()).

    Exemple :
        trajets = [
            {"quartier_depart": "Bacongo", "prix_place": 500},
            {"quartier_depart": "Bacongo", "prix_place": 400},
            {"quartier_depart": "Bacongo", "prix_place": 600},
        ]
        calculer_prix_moyen_par_quartier(trajets)
        -> {"Bacongo": 500}
        (moyenne de 500, 400 et 600 = 500)
    """
    # TODO : à compléter
    pass


def identifier_trajet_le_plus_reserve(trajets, reservations):
    """
    Identifie le trajet ayant reçu le plus de réservations actives
    (statut "effectue" ou "en_attente" — pas "annule"). Utilisée pour
    l'encart "Trajet vedette" du tableau de bord.

    Paramètres :
        trajets      : liste de dict trajet, chacun avec "id" (int),
                       "quartier_depart" (str) et "quartier_arrivee" (str)
        reservations : liste de dict réservation, chacun avec "trajet_id"
                       (int) et "statut" (str)

    Retourne :
        un dictionnaire avec EXACTEMENT ces 3 clés :
        {
            "trajet_id": int,
            "trajet_libelle": str,       # ex. "Bacongo → Poto-Poto"
            "nombre_reservations": int
        }

        Si aucune réservation active n'existe, retourner None.
        En cas d'égalité entre plusieurs trajets, retourner celui avec le
        plus petit trajet_id.

    Exemple :
        trajets = [
            {"id": 1, "quartier_depart": "Bacongo", "quartier_arrivee": "Poto-Poto"},
            {"id": 2, "quartier_depart": "Moungali", "quartier_arrivee": "Bacongo"},
        ]
        reservations = [
            {"trajet_id": 1, "statut": "effectue"},
            {"trajet_id": 1, "statut": "effectue"},
            {"trajet_id": 2, "statut": "effectue"},
        ]
        identifier_trajet_le_plus_reserve(trajets, reservations)
        -> {"trajet_id": 1, "trajet_libelle": "Bacongo → Poto-Poto", "nombre_reservations": 2}
    """
    # TODO : à compléter
    pass


def calculer_indicateurs_dashboard(trajets, reservations, conducteurs):
    """
    Calcule les 4 indicateurs principaux affichés en haut du tableau de
    bord. C'est la fonction la plus visible de tout le projet : elle
    alimente les 4 cartes chiffrées que la communauté verra en premier.

    Paramètres :
        trajets      : liste de dict trajet, chacun avec "places_dispo" (int)
        reservations : liste de dict réservation, chacun avec "statut" (str)
        conducteurs  : liste de dict conducteur, chacun avec "note" (float)

    Retourne :
        un dictionnaire avec EXACTEMENT ces 4 clés :
        {
            "total_trajets_disponibles": int,   # trajets avec places_dispo >= 1
            "total_conducteurs_actifs": int,    # nombre total de conducteurs
            "total_reservations_actives": int,  # statut "effectue" + "en_attente"
            "note_moyenne_conducteurs": float   # moyenne des notes, arrondie à 1 décimale
        }

        Si la liste conducteurs est vide, note_moyenne_conducteurs vaut 0.0.

    IMPORTANT : cette fonction NE DOIT PAS appeler d'autres fonctions de
    logic.py (ni filtrer_trajets_disponibles, ni compter_reservations_par_trajet,
    ni top_conducteurs_par_note). Recalculez chaque indicateur vous-même,
    en local, pour que cette fonction reste indépendante des autres — un
    test vérifie explicitement cette indépendance.

    Exemple :
        trajets = [{"places_dispo": 3}, {"places_dispo": 0}, {"places_dispo": 2}]
        reservations = [{"statut": "effectue"}, {"statut": "en_attente"}, {"statut": "annule"}]
        conducteurs = [{"note": 4.5}, {"note": 4.9}, {"note": 4.7}]
        calculer_indicateurs_dashboard(trajets, reservations, conducteurs)
        -> {
            "total_trajets_disponibles": 2,
            "total_conducteurs_actifs": 3,
            "total_reservations_actives": 2,
            "note_moyenne_conducteurs": 4.7
        }
    """
    # TODO : à compléter
    pass


# ========================================================================
# ZONE D — Comptes & authentification
# ========================================================================

def verifier_telephone_disponible(comptes, telephone):
    """
    Vérifie qu'aucun compte existant n'utilise déjà ce numéro de
    téléphone. Utilisée avant la création d'un compte, pour empêcher
    les doublons d'inscription.

    Paramètres :
        comptes   : liste de dict, chacun avec une clé "telephone" (str)
        telephone : numéro à vérifier (str), ex. "066123456"

    Retourne :
        True si aucun compte de la liste n'a ce téléphone, False sinon.

    Exemple :
        comptes = [{"id": 1, "telephone": "066123456"}]
        verifier_telephone_disponible(comptes, "066123456") -> False
        verifier_telephone_disponible(comptes, "055999999") -> True
    """
    # TODO : à compléter
    pass


def trouver_compte_par_telephone(comptes, telephone):
    """
    Retourne le compte correspondant à un numéro de téléphone donné.
    Utilisée lors du login pour récupérer le compte dont il faut vérifier
    le mot de passe.

    Paramètres :
        comptes   : liste de dict, chacun avec une clé "telephone" (str)
        telephone : numéro recherché (str), ex. "066123456"

    Retourne :
        le dict compte dont "telephone" correspond exactement, ou None
        si aucun compte ne correspond.

    Exemple :
        comptes = [{"id": 1, "telephone": "066123456", "nom": "Franck"}]
        trouver_compte_par_telephone(comptes, "066123456")
        -> {"id": 1, "telephone": "066123456", "nom": "Franck"}
        trouver_compte_par_telephone(comptes, "055999999") -> None
    """
    # TODO : à compléter
    pass
