# Rapport Backend — BraCovoit / Tokeyi

**Projet :** Covoiturage inter-quartiers, Brazzaville  
**Rôle :** Lead Data — Responsable de l'équipe Backend  
**Date :** 1er août 2026  
**Statut :** En cours de développement (phase de complétion des fonctions)  
**Branche active :** `feature/backend/functions`  
**Branche cible :** `develop` (intégration) → `main` (production)

---

## 0. Branches du projet

```
main                          # Production
  └── develop                 # Intégration (cible PR)
       ├── feature/backend/functions          ← BRANCHE ACTIVE
       ├── feature/frontend/setup-design-system
       ├── feature/frontend/fs1-accueil
       ├── feature/frontend/page-recherche
       ├── feature/frontend/proposer-trajet
       └── feature/frontend/ci-quality-gates
```

**Flux de travail :** Chaque fonctionnalité est développée dans une branche `feature/*`, fusionnée dans `develop` via Pull Request, puis `develop` est mergée dans `main` pour les livraisons.

---

## 0.1 Historique des commits (branche backend uniquement)

| Hash | Date | Auteur | Message |
|---|---|---|---|
| `10be192` | 2026-08-01 | Malkyma | feature: Zone C, function 5: calculate dashboard indicators |
| `0417d8b` | 2026-08-01 | Malkyma | feature: Zone C, function 4: identify most reserved route |
| `1c58740` | 2026-08-01 | Malkyma | feature: Zone C, function 3: calculate average price per district |
| `3cdde10` | 2026-08-01 | Malkyma | feature: Zone C, function 2: top driver per note |
| `09ece07` | 2026-08-01 | Malkyma | feature: Zone C, function 1: count route by starting district |
| `7c749fc` | 2026-08-01 | Malkyma | feature: Zone B, function 2: verify available place |
| `19f4d2d` | 2026-08-01 | Malkyma | feature: Zone A, function 5: sort by price (ascending) |
| `feedcc3` | 2026-08-01 | Malkyma | feature: Zone A, function 4: sort by hour |
| `95808a1` | 2026-08-01 | Malkyma | feature: Zone A, function 1: filter available route |

**Auteur backend :** Malkyma(Lead DATA 1) et Sublime999 (Lead DATA 2) — 9 commits sur la branche `feature/backend/functions`

## 1. Architecture générale

### Stack technique

| Technologie | Version | Usage |
|---|---|---|
| Python | 3.12 | Langage backend |
| Flask | 3.0.0 | Framework web REST |
| Flask-CORS | 4.0.0 | Gestion des CORS (toutes origines) |
| pytest | 7.4.3 | Tests unitaires |
| Werkzeug | (incluse) | Hachage des mots de passe |
| JSON | — | Stockage de données (fichiers plats) |

### Architecture en 3 couches (strict)

```
app.py              → Routes Flask, validation des requêtes
  ↓
controllers.py      → Orchestration, lecture/écriture JSON, appels à logic.py
  ↓
logic.py            → Fonctions métier pures (À COMPLÉTER PAR L'ÉQUIPE)
```

**Règles strictes :**
- `app.py` et `controllers.py` sont marqués **NE PAS MODIFIER**
- `logic.py` contient 17 fonctions à compléter par l'équipe Data Science
- `logic.py` ne doit contenir que des fonctions pures (pas d'I/O, pas de Flask, pas de DB)

---

## 2. Points d'entrée (API)

**Base URL :** `http://localhost:5000`

| Méthode | Route | Statut | Description |
|---|---|---|---|
| GET | `/` |  OK | Informations API, liste des routes |
| GET | `/api/quartiers` |  OK | Liste des 8 quartiers de Brazzaville |
| GET | `/api/trajets` |  Partiel | Liste des trajets (dépend des fonctions Zone A) |
| GET | `/api/trajets/<id>` |  Partiel | Détail d'un trajet (dépend de `verifier_place_disponible`) |
| POST | `/api/reservations` |  Partiel | Créer une réservation (dépend de `verifier_place_disponible`) |
| GET | `/api/reservations/<tel>` |  Bloqué | Historique passager (dépend de `historique_reservations_passager`) |
| GET | `/api/dashboard` |  Partiel | Indicateurs tableau de bord (dépend de Zone C) |
| POST | `/api/inscription` |  Bloqué | Créer un compte (dépend de `verifier_telephone_disponible`) |
| POST | `/api/login` |  Bloqué | Authentification (dépend de `trouver_compte_par_telephone`) |

**Légende :**
-  OK : Fonctionne sans dépendance extérieure
-  Partiel : Fonctionne partiellement (certaines fonctions déjà implémentées)
-  Bloqué : Nécessite des fonctions TODO de `logic.py`

---

## 3. Modèle de données (fichier JSON)

### `data/trajets.json` — Données principales

**Quartiers :** 8 quartiers de Brazzaville
```json
["Bacongo", "Poto-Poto", "Moungali", "Talangaï", "Mfilou", "Makélékélé", "Ouenzé", "Kintélé"]
```

**Conducteurs :** 8 conducteurs seedés
| Champ | Type | Description |
|---|---|---|
| `id` | int | Identifiant unique |
| `nom` | str | Nom complet |
| `telephone` | str | Numéro de téléphone |
| `note` | float | Note moyenne (0–5) |
| `trajets_effectues` | int | Nombre de trajets réalisés |
| `vehicule` | str | Modèle de véhicule |

**Trajets :** 15 trajets seedés
| Champ | Type | Description |
|---|---|---|
| `id` | int | Identifiant unique |
| `conducteur_id` | int | Référence au conducteur |
| `quartier_depart` | str | Quartier de départ |
| `quartier_arrivee` | str | Quartier d'arrivée |
| `date` | str | Date au format ISO |
| `heure` | str | Heure au format "HH:MM" |
| `places_dispo` | int | Capacité initiale |
| `prix_place` | int | Prix en FCFA |
| `commentaire` | str | Optionnel |

**Réservations :** 20 réservations seedées
| Champ | Type | Description |
|---|---|---|
| `id` | int | Identifiant unique |
| `trajet_id` | int | Référence au trajet |
| `passager_nom` | str | Nom du passager |
| `passager_tel` | str | Téléphone du passager |
| `date_reservation` | str | Date de réservation |
| `statut` | str | `"effectue"`, `"en_attente"`, `"annule"` |

### `data/comptes.json` — Comptes utilisateurs

| Champ | Type | Description |
|---|---|---|
| `id` | int | Identifiant unique |
| `nom` | str | Nom complet |
| `telephone` | str | Numéro de téléphone (unique) |
| `mot_de_passe_hash` | str | Mot de passe haché (Werkzeug) |

**État actuel :** Vide (les comptes sont créés via l'inscription).

---

## 4. Avancement des fonctions `logic.py`

### Zone A — Recherche & disponibilité (5 fonctions)

| # | Fonction | Statut | Tests |
|---|---|---|---|
| 1 | `filtrer_trajets_disponibles` |  **FAIT** | 3 tests passent |
| 2 | `filtrer_par_quartier_depart` |  **TODO** | 2 tests échouent |
| 3 | `filtrer_par_trajet_complet` |  **TODO** | 1 test échoue |
| 4 | `trier_par_heure` |  **FAIT** | 2 tests passent |
| 5 | `trier_par_prix_croissant` |  **FAIT** | 1 test passe |

**Total Zone A : 3/5 fonctions complétées, 6/9 tests verts**

### Zone B — Réservations & suivi (5 fonctions)

| # | Fonction | Statut | Tests |
|---|---|---|---|
| 6 | `compter_reservations_par_trajet` |  **TODO** | 2 tests échouent |
| 7 | `verifier_place_disponible` |  **FAIT** | 3 tests passent |
| 8 | `filtrer_reservations_par_statut` |  **TODO** | 1 test échoue |
| 9 | `historique_reservations_passager` |  **TODO** | 1 test échoue |
| 10 | `calculer_taux_annulation` |  **TODO** | 3 tests échouent |

**Total Zone B : 1/5 fonctions complétées, 3/10 tests verts**

### Zone C — Statistiques & tableau de bord (5 fonctions)

| # | Fonction | Statut | Tests |
|---|---|---|---|
| 11 | `compter_trajets_par_quartier_depart` |  **FAIT** | 2 tests passent |
| 12 | `top_conducteurs_par_note` |  **FAIT** | 2 tests passent |
| 13 | `calculer_prix_moyen_par_quartier` |  **FAIT** | 1 test passe |
| 14 | `identifier_trajet_le_plus_reserve` |  **FAIT** | 2 tests passent |
| 15 | `calculer_indicateurs_dashboard` |  **FAIT** | 2 tests passent (+ indépendance) |

**Total Zone C : 5/5 fonctions complétées, 9/9 tests verts** 

### Zone D — Comptes & authentification (2 fonctions)

| # | Fonction | Statut | Tests |
|---|---|---|---|
| 16 | `verifier_telephone_disponible` |  **TODO** | 3 tests échouent |
| 17 | `trouver_compte_par_telephone` |  **TODO** | 2 tests échouent |

**Total Zone D : 0/2 fonctions complétées, 0/5 tests verts**

---

## 5. Bilan global des tests

### Résumé

| Zone | Fonctions | Fait | TODO | Tests | Verts | Rouges |
|---|---|---|---|---|---|---|
| Zone A | 5 | 3 | 2 | 9 | 6 | 3 |
| Zone B | 5 | 1 | 4 | 10 | 3 | 7 |
| Zone C | 5 | 5 | 0 | 9 | 9 | 0 |
| Zone D | 2 | 0 | 2 | 5 | 0 | 5 |
| **Total** | **17** | **9** | **8** | **33** | **18** | **15** |

**Progression globale : 52.9% des fonctions complétées, 54.5% des tests verts**

### Répartition par statut

```
 Complétées :  9 / 17  (52.9%)
 TODO :        8 / 17  (47.1%)
```

---

## 6. Authentification & Sécurité

- **Inscription :** Hachage des mots de passe via `werkzeug.security.generate_password_hash()` (PBKDF2-SHA256)
- **Connexion :** Vérification via `check_password_hash()`
- **Session :** Côté client uniquement (stockage dans `localStorage` côté frontend)
- **Pas de JWT, pas de cookies, pas de middleware d'autorisation**
- **CORS :** Toutes origines autorisées (mode développement)
- **Protection anti-doublon :** `verifier_telephone_disponible` empêche les inscriptions multiples avec le même numéro

---

## 7. Gestion des erreurs

- **Handler global** (`@app.errorhandler(Exception)`) : capture toutes les exceptions
- **Format de réponse :** JSON avec clés `"erreur"` et `"detail_technique"`
- **Propagation désactivée** (`PROPAGATE_EXCEPTIONS = False`) : évite les pages HTML de debug Werkzeug
- **Codes HTTP :** 400 (champs manquants), 401 (auth échouée), 404 (ressource introuvable), 500 (erreur interne)

---

## 8. Tests

### Commande d'exécution
```bash
cd backend
python -m pytest -v
```

### Couverture des tests
- 33 tests unitaires couvrant les 17 fonctions de `logic.py`
- Test spécial d'indépendance : `test_calculer_indicateurs_independance` vérifie que `calculer_indicateurs_dashboard` n'appelle pas d'autres fonctions de `logic.py`
- Tests de cas limites : listes vides, trajets complets, annulations, doublons

---

## 9. TODO — Fonctions restantes (priorité)

### Priorité Haute — Bloquent des routes API

| # | Fonction | Route bloquée |
|---|---|---|
| 16 | `verifier_telephone_disponible` | `POST /api/inscription` |
| 17 | `trouver_compte_par_telephone` | `POST /api/login` |
| 9 | `historique_reservations_passager` | `GET /api/reservations/<tel>` |

### Priorité Moyenne — Améliorent la recherche

| # | Fonction | Route améliorée |
|---|---|---|
| 2 | `filtrer_par_quartier_depart` | `GET /api/trajets?depart=` |
| 3 | `filtrer_par_trajet_complet` | `GET /api/trajets?depart=&arrivee=` |

### Priorité Standard — Complètent les fonctionnalités

| # | Fonction | Usage |
|---|---|---|
| 6 | `compter_reservations_par_trajet` | Statistiques internes |
| 8 | `filtrer_reservations_par_statut` | Filtres côté dashboard |
| 10 | `calculer_taux_annulation` | Indicateur dashboard |

---

## 10. Répartition des tâches

### Lead Data — Malkyma  TERMINÉ

| Zone | Fonctions | Statut |
|---|---|---|
| Zone A | `filtrer_trajets_disponibles`, `trier_par_heure`, `trier_par_prix_croissant` |  FAIT |
| Zone B | `verifier_place_disponible` |  FAIT |
| Zone C | `compter_trajets_par_quartier_depart`, `top_conducteurs_par_note`, `calculer_prix_moyen_par_quartier`, `identifier_trajet_le_plus_reserve`, `calculer_indicateurs_dashboard` |  FAIT |

**Total : 9 fonctions complétées — 18 tests verts**

### Data 2 — À faire

| Zone | Fonction | Tests |
|---|---|---|
| Zone A | `filtrer_par_quartier_depart` | 2 |
| Zone A | `filtrer_par_trajet_complet` | 1 |
| Zone B | `compter_reservations_par_trajet` | 2 |
| Zone B | `filtrer_reservations_par_statut` | 1 |
| Zone B | `historique_reservations_passager` | 1 |
| Zone B | `calculer_taux_annulation` | 3 |
| Zone D | `verifier_telephone_disponible` | 3 |
| Zone D | `trouver_compte_par_telephone` | 2 |

**Total : 8 fonctions restantes — 15 tests à passer au vert**

### Prochaines étapes
1. Compléter les fonctions Zone D (débloque l'inscription et le login)
2. Compléter les fonctions Zone A (filtres de recherche)
3. Compléter les fonctions Zone B (réservations et historique)
4. Exécuter `python -m pytest -v` et viser **33/33 tests verts**
5. Tester manuellement les routes API avec le navigateur

---

## 11. Références

- **Fichier à compléter :** `backend/logic.py`
- **Fichiers NE PAS MODIFIER :** `backend/app.py`, `backend/controllers.py`
- **Données :** `backend/data/trajets.json`, `backend/data/comptes.json`
- **Tests :** `backend/tests/test_logic.py` (33 tests)
- **README :** `README.md` (instructions complètes)
- **Documentation API :** En-tête de `app.py` (lignes 1-15)