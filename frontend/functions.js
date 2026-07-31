/**
 * functions.js — Fonctions JS pures pour le projet Covoiturage
 *
 * >>> À COMPLÉTER par l'équipe Full Stack <<<
 *
 * Chaque personne complète 2 fonctions (voir répartition dans le README).
 *
 * RÈGLE D'OR : ces fonctions sont PURES. Elles reçoivent des paramètres,
 * elles retournent une valeur avec `return`. Pas de fetch, pas de document.
 * getElementById, pas de DOM. Le DOM est déjà géré dans main.js — vous
 * n'y touchez pas.
 *
 * Pour vérifier votre travail : ouvrez functions.test.html dans le navigateur.
 * Tous les tests doivent passer au VERT.
 */

// ============================================================================
// Dev FS1 — page Accueil
// ============================================================================

function compterTrajetsAujourdhui(trajets, dateAujourdhui) {
    /**
     * Compte le nombre de trajets prévus pour la date donnée.
     * @param {Array} trajets - liste d'objets avec une clé "date" (ex: "2026-07-27")
     * @param {string} dateAujourdhui - date au format "AAAA-MM-JJ"
     * @return {number} - nombre de trajets à cette date
     * Exemple : compterTrajetsAujourdhui([{date:"2026-07-27"},{date:"2026-07-28"}], "2026-07-27") → 1
     */
    // TODO
}

function formaterQuartierPrincipal(compteParQuartier) {
    /**
     * Retourne le nom du quartier qui a le plus de trajets, sous forme lisible.
     * @param {Object} compteParQuartier - ex: {"Bacongo": 5, "Moungali": 3, "Poto-Poto": 8}
     * @return {string} - ex: "Poto-Poto (8 trajets)"
     * Si l'objet est vide, retourne "Aucun trajet".
     */
    // TODO
}

// ============================================================================
// Dev FS2 — page Recherche
// ============================================================================

function filtrerParQuartierDepart(trajets, quartier) {
    /**
     * Retourne les trajets partant du quartier donné.
     * @param {Array} trajets - liste d'objets trajet avec "quartier_depart"
     * @param {string} quartier - nom du quartier
     * @return {Array} - trajets filtrés
     * Si quartier est vide ou null, retourne tous les trajets.
     */
    // TODO
}

function rechercherParMotCle(trajets, motCle) {
    /**
     * Recherche les trajets dont le quartier_depart, quartier_arrivee ou
     * commentaire contient le mot-clé (insensible à la casse).
     * @param {Array} trajets - liste de trajets
     * @param {string} motCle - mot recherché
     * @return {Array} - trajets correspondants
     * Si motCle est vide, retourne tous les trajets.
     */
    // TODO
}

// ============================================================================
// Dev FS3 — page Détail trajet
// ============================================================================

function formaterPrix(prix) {
    /**
     * Formate un prix en FCFA avec séparateur de milliers.
     * @param {number} prix - prix en FCFA (ex: 5000)
     * @return {string} - "5 000 FCFA"
     * Exemple : formaterPrix(500) → "500 FCFA", formaterPrix(1500) → "1 500 FCFA"
     */
    // TODO
}

function formaterHeure(heure) {
    /**
     * Formate une heure au format "HHhMM" à partir d'une heure "HH:MM".
     * @param {string} heure - format "HH:MM" (ex: "07:30")
     * @return {string} - "07h30"
     */
    // TODO
}

// ============================================================================
// Dev FS4 — page Proposer un trajet
// ============================================================================

function validerFormulaireProposer(formulaire) {
    /**
     * Valide le formulaire de proposition de trajet.
     * @param {Object} formulaire - avec les clés : quartier_depart,
     *   quartier_arrivee, heure, places_dispo, prix_place
     * @return {Object} - {valide: true/false, erreurs: [liste de messages]}
     *
     * Règles :
     * - quartier_depart et quartier_arrivee obligatoires et différents
     * - heure obligatoire au format "HH:MM"
     * - places_dispo entre 1 et 8
     * - prix_place > 0
     */
    // TODO
}

function formaterMessageConfirmation(nom, quartierDepart, quartierArrivee, heure) {
    /**
     * Génère le message de confirmation après réservation.
     * @return {string} - message formaté
     * Exemple :
     *   formaterMessageConfirmation("Marie", "Bacongo", "Poto-Poto", "07:30")
     *   → "Bonjour Marie, votre réservation pour Bacongo → Poto-Poto à 07:30 a été enregistrée."
     */
    // TODO
}

// ============================================================================
// Dev FS5 — page Mes trajets
// ============================================================================

function filtrerReservationsParStatut(reservations, statut) {
    /**
     * Filtre les réservations par statut.
     * @param {Array} reservations - liste de réservations
     * @param {string} statut - "effectue", "en_attente", "annule" ou "" pour toutes
     * @return {Array} - réservations correspondantes
     */
    // TODO
}

function calculerTotalDepenseParPassager(reservations) {
    /**
     * Calcule le total dépensé par un passager sur ses réservations non annulées.
     * @param {Array} reservations - chaque réservation a une clé "trajet"
     *   qui contient {prix_place: number} et une clé "statut"
     * @return {number} - somme des prix_place des réservations non "annule"
     * Exemple :
     *   3 réservations : 500 (effectue), 700 (en_attente), 400 (annule)
     *   → 1200
     */
    // TODO
}

// ============================================================================
// Dev FS6 — pages Dashboard + Confirmation (intégrateur)
// ============================================================================

function calculerPourcentageOccupation(placesOccupees, placesTotales) {
    /**
     * Calcule le pourcentage d'occupation d'un trajet.
     * @param {number} placesOccupees - places réservées
     * @param {number} placesTotales - places totales du trajet
     * @return {number} - pourcentage arrondi (0 à 100)
     * Exemple : 2 places sur 4 → 50
     * Si placesTotales est 0, retourne 0.
     */
    // TODO
}

function getBadgeDisponibilite(placesRestantes) {
    /**
     * Retourne le libellé et la classe CSS d'un badge de disponibilité.
     * @param {number} placesRestantes - nombre de places restantes
     * @return {Object} - {libelle: string, classe: string}
     *
     * Règles :
     * - 0 place  → {libelle: "Complet", classe: "badge-complet"}
     * - 1 place  → {libelle: "1 place", classe: "badge-limite"}
     * - 2+ places → {libelle: "N places", classe: "badge-dispo"}  (N = placesRestantes)
     */
    // TODO
}

// ============================================================================
// Dev FS7 — pages Inscription + Login
// ============================================================================

function validerFormulaireInscription(formulaire) {
    /**
     * Valide le formulaire d'inscription.
     * @param {Object} formulaire - avec les clés : nom, telephone, mot_de_passe
     * @return {Object} - {valide: true/false, erreurs: [liste de messages]}
     *
     * Règles :
     * - nom obligatoire (non vide après trim)
     * - telephone obligatoire, au moins 9 chiffres
     * - mot_de_passe obligatoire, au moins 4 caractères
     */
    // TODO
}

function validerFormulaireLogin(formulaire) {
    /**
     * Valide le formulaire de connexion.
     * @param {Object} formulaire - avec les clés : telephone, mot_de_passe
     * @return {Object} - {valide: true/false, erreurs: [liste de messages]}
     *
     * Règles :
     * - telephone obligatoire
     * - mot_de_passe obligatoire
     */
    // TODO
}

// ============================================================================
// NE PAS MODIFIER : export pour les tests
// ============================================================================
if (typeof module !== "undefined" && module.exports) {
    module.exports = {
        compterTrajetsAujourdhui, formaterQuartierPrincipal,
        filtrerParQuartierDepart, rechercherParMotCle,
        formaterPrix, formaterHeure,
        validerFormulaireProposer, formaterMessageConfirmation,
        filtrerReservationsParStatut, calculerTotalDepenseParPassager,
        calculerPourcentageOccupation, getBadgeDisponibilite,
        validerFormulaireInscription, validerFormulaireLogin,
    };
}
