"""
app.py — Point d'entrée Flask du projet Covoiturage.

*** NE PAS MODIFIER *** — ce fichier connecte l'API aux fonctions logic.py.

Routes :
  GET  /api/trajets                 → liste des trajets disponibles (avec filtres)
  GET  /api/trajets/<id>            → détail d'un trajet
  POST /api/reservations            → créer une réservation
  GET  /api/reservations/<tel>      → historique d'un passager
  GET  /api/dashboard               → indicateurs du tableau de bord
  GET  /api/quartiers               → liste des quartiers
  POST /api/inscription             → créer un compte
  POST /api/login                   → se connecter
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from controllers import (
    lister_trajets_disponibles, get_trajet, creer_reservation,
    lister_reservations_passager, get_dashboard, lister_quartiers,
    creer_compte, login,
)

app = Flask(__name__)
CORS(app)

# Empêche le débogueur interactif Werkzeug (page HTML brute) de répondre
# aux erreurs : tant que certaines fonctions de logic.py sont encore à
# `pass`, plusieurs routes lèvent une exception Python. Sans ce réglage,
# le navigateur reçoit une page HTML de débogage à la place du JSON
# attendu, ce qui casse le fetch() côté frontend de façon peu lisible.
# Avec ce réglage, l'erreur s'affiche proprement dans le terminal (trace
# complète, comme avant) ET le navigateur reçoit un message JSON clair.
app.config["PROPAGATE_EXCEPTIONS"] = False


@app.errorhandler(Exception)
def gerer_erreur(erreur):
    import traceback
    traceback.print_exc()  # trace complète toujours visible dans le terminal
    return jsonify({
        "erreur": "Cette route a échoué car une fonction de logic.py n'est "
                   "pas encore implémentée (ou contient une erreur). "
                   "Regardez le terminal où tourne 'python app.py' pour le "
                   "détail exact (traceback Python).",
        "detail_technique": str(erreur),
    }), 500


@app.route("/", methods=["GET"])
def route_racine():
    return jsonify({
        "message": "API BraCovoit — Covoiturage inter-quartiers, Brazzaville. "
                    "Ceci est l'API seule (JSON). Le site (pages HTML) se lance "
                    "séparément — voir le README, section \"Lancer le projet en local\".",
        "routes_disponibles": [
            "/api/trajets", "/api/trajets/<id>", "/api/reservations",
            "/api/reservations/<tel>", "/api/dashboard", "/api/quartiers",
            "/api/inscription", "/api/login",
        ],
    })


@app.route("/api/trajets", methods=["GET"])
def route_trajets():
    depart = request.args.get("depart")
    arrivee = request.args.get("arrivee")
    return jsonify(lister_trajets_disponibles(depart, arrivee))


@app.route("/api/trajets/<int:trajet_id>", methods=["GET"])
def route_trajet_detail(trajet_id):
    data = get_trajet(trajet_id)
    if data is None:
        return jsonify({"erreur": "Trajet introuvable"}), 404
    return jsonify(data)


@app.route("/api/reservations", methods=["POST"])
def route_reservation():
    payload = request.get_json(force=True) or {}
    trajet_id = payload.get("trajet_id")
    passager_nom = payload.get("passager_nom")
    passager_tel = payload.get("passager_tel")
    if not all([trajet_id, passager_nom, passager_tel]):
        return jsonify({"erreur": "Champs manquants"}), 400
    result = creer_reservation(int(trajet_id), passager_nom, passager_tel)
    if not result.get("ok"):
        return jsonify(result), 400
    return jsonify(result), 201


@app.route("/api/reservations/<tel>", methods=["GET"])
def route_reservations_passager(tel):
    return jsonify(lister_reservations_passager(tel))


@app.route("/api/dashboard", methods=["GET"])
def route_dashboard():
    return jsonify(get_dashboard())


@app.route("/api/quartiers", methods=["GET"])
def route_quartiers():
    return jsonify(lister_quartiers())


@app.route("/api/inscription", methods=["POST"])
def route_inscription():
    payload = request.get_json(force=True) or {}
    nom = payload.get("nom")
    telephone = payload.get("telephone")
    mot_de_passe = payload.get("mot_de_passe")
    if not all([nom, telephone, mot_de_passe]):
        return jsonify({"erreur": "Champs manquants"}), 400
    result = creer_compte(nom, telephone, mot_de_passe)
    if not result.get("ok"):
        return jsonify(result), 400
    return jsonify(result), 201


@app.route("/api/login", methods=["POST"])
def route_login():
    payload = request.get_json(force=True) or {}
    telephone = payload.get("telephone")
    mot_de_passe = payload.get("mot_de_passe")
    if not all([telephone, mot_de_passe]):
        return jsonify({"erreur": "Champs manquants"}), 400
    result = login(telephone, mot_de_passe)
    if not result.get("ok"):
        return jsonify(result), 401
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
