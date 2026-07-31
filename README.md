# BraCovoit — Covoiturage inter-quartiers, Brazzaville

Bienvenue dans votre startup. Ce dépôt est le **squelette** de l'application : un mini-site de 9 pages pour organiser le covoiturage entre habitants des quartiers de Brazzaville. La structure est déjà en place ; **votre équipe complète les fonctions manquantes et construit les pages**.

Vous avez **quelques jours** pour ce projet.

## Lancer le projet en local

**1. Démarrer l'API (un seul terminal, à laisser ouvert)**

```bash
cd backend
pip install -r requirements.txt
python app.py
```

L'API tourne sur `http://localhost:5000`. Laissez ce terminal ouvert tout le temps où vous travaillez.

**2. Ouvrir le site**

**Si vous utilisez VS Code, l'extension Live Server fonctionne aussi très bien (clic droit sur le fichier HTML → "Open with Live Server").**

**C'est tout : un seul terminal pour l'API, et vous ouvrez vos pages HTML directement.** Tant que `python app.py` tourne, n'importe quelle page du site peut appeler l'API normalement.

### Si une page ne s'affiche pas comme attendu

- **Une carte ou une section reste vide** : c'est normal si la fonction

Python ou JavaScript correspondante n'est pas encore codée. Les autres   sections de la page continuent de s'afficher normalement — seule la   section concernée reste vide en attendant votre code.

- **Un message d'erreur apparaît sur la page** : lisez-le, il indique

quelle fonction regarder. Le détail technique complet (traceback   Python) est toujours visible dans le terminal où tourne `python app.py`.

- **Rien ne s'affiche du tout** : vérifiez d'abord que le terminal de

l'API est bien ouvert et actif (pas d'erreur affichée dedans). Si vous   venez de modifier `main.js` ou `functions.js`, faites un rafraîchissement   forcé de la page (Ctrl+Maj+R ou Cmd+Maj+R) — le navigateur met parfois   en cache l'ancienne version du fichier.

## Qui fait quoi

| Parcours | Effectif | Vous complétez | Vous ne touchez PAS |
| --- | --- | --- | --- |
| **Data Science** | 1 à 3 personnes | `backend/logic.py` (17 fonctions) | `app.py`, `controllers.py` |
| **Full Stack** | 7 personnes | *voir répartition ci-dessous* | `main.js` |

**Le nommage des champs est déjà fixé dans le code** (docstrings de `logic.py`, structure de `data/trajets.json`, IDs des éléments HTML). Vous n'avez pas à deviner ces noms — regardez les docstrings et le jeu de données pour comprendre le contrat technique attendu.

## Répartition Full Stack

Chaque page est dans son propre sous-dossier avec son fichier CSS dédié. L'essentiel de votre note porte sur vos **pages HTML/CSS** (structure sémantique, box model, Flexbox/Grid, responsive mobile/tablette/desktop). Chacun complète aussi **2 fonctions JS** dans `frontend/functions.js`.

| Qui | Dossier & page | Fonctions JS |
| --- | --- | --- |
| Dev FS1 | `frontend/accueil/index.html` + `accueil.css` — page d'accueil, hero + indicateurs clés | `compterTrajetsAujourdhui`, `formaterQuartierPrincipal` |
| Dev FS2 | `frontend/recherche/recherche.html` + `recherche.css` — recherche et filtres | `filtrerParQuartierDepart`, `rechercherParMotCle` |
| Dev FS3 | `frontend/trajet/trajet.html` + `trajet.css` — détail d'un trajet + réservation | `formaterPrix`, `formaterHeure` |
| Dev FS4 | `frontend/proposer/proposer.html` + `proposer.css` — formulaire conducteur | `validerFormulaireProposer`, `formaterMessageConfirmation` |
| Dev FS5 | `frontend/mes-trajets/mes-trajets.html` + `mes-trajets.css` — historique passager | `filtrerReservationsParStatut`, `calculerTotalDepenseParPassager` |
| Dev FS6 | `frontend/dashboard/dashboard.html` + `dashboard.css` **ET** `frontend/confirmation/confirmation.html` + `confirmation.css` | `calculerPourcentageOccupation`, `getBadgeDisponibilite` |
| Dev FS7 | `frontend/inscription/inscription.html` + `inscription.css` **ET** `frontend/login/login.html` + `login.css` | `validerFormulaireInscription`, `validerFormulaireLogin` |

Chaque page contient des commentaires `<!-- TODO -->` indiquant le travail attendu, avec le layout, les éléments à construire et les classes CSS que `main.js` utilise déjà pour injecter le contenu dynamique. **Les éléments marqués "NE PAS MODIFIER" (IDs, scripts, formulaires) sont le câblage vers le backend — ne les changez pas, sinon les données ne s'afficheront plus.**

## Équipe Data Science — workflow

```bash
cd backend
pip install -r requirements.txt
python -m pytest -v        # au départ : quelques tests verts, la majorité rouges
```

Ouvrez `backend/logic.py` : la première fonction (`filtrer*trajets*disponibles`) est déjà résolue et commentée — regardez-la pour comprendre le style de code et le niveau de détail attendu, avant de compléter les 16 autres. Complétez-les (4 zones, à répartir selon votre effectif), relancez les tests jusqu'au **VERT**.

Pour vérifier vos résultats via l'API une fois les tests au vert, lancez `python app.py` (voir "Lancer le projet en local" ci-dessus) puis testez dans le navigateur :

```
http://localhost:5000/api/trajets
http://localhost:5000/api/trajets/1
http://localhost:5000/api/dashboard
http://localhost:5000/api/quartiers
http://localhost:5000/api/reservations/067111222
```

L'inscription et le login se testent en POST (par exemple avec `curl` ou un client HTTP) :

```
POST http://localhost:5000/api/inscription   {"nom": "...", "telephone": "...", "mot_de_passe": "..."}
POST http://localhost:5000/api/login          {"telephone": "...", "mot_de_passe": "..."}
```

## Équipe Full Stack — workflow

1. Ouvrez `frontend/functions.test.html` dans le navigateur → la majorité

des tests sont rouges au départ (27 tests, 2 par personne).

1. Complétez vos 2 fonctions dans `frontend/functions.js`.
2. Construisez vos pages HTML/CSS dans votre sous-dossier.
3. Pour voir le rendu de votre page connectée aux vraies données, suivez

la section "Lancer le projet en local" ci-dessus (backend démarré,    puis ouvrez simplement votre fichier HTML).

## La règle d'or (JS)

Fonctions **pures** : des paramètres entrent, une valeur sort (`return`). Pas de DOM, pas de `fetch` — tout est déjà branché dans `main.js`.

## Le jeu de données

`backend/data/trajets.json` contient 8 quartiers, 8 conducteurs, 15 trajets et 20 réservations couvrant avril à juillet 2026. Ne modifiez pas ce fichier — vos calculs doivent fonctionner avec ces données telles quelles.

## Contexte du produit

BraCovoit met en relation des habitants de Brazzaville qui font le même trajet au même moment : un conducteur qui a des places libres dans sa voiture, et des passagers qui cherchent un trajet moins cher et plus flexible qu'un taxi. Le site couvre 8 quartiers de Brazzaville (Bacongo, Poto-Poto, Moungali, Talangaï, Mfilou, Makélékélé, Ouenzé, Kintélé), avec des trajets essentiellement concentrés sur les créneaux du matin (7h-9h) et du soir (17h-19h).

Bonne construction.
