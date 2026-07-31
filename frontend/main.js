/**
 * main.js — Câblage réseau + DOM pour toutes les pages
 *
 * *** NE PAS MODIFIER ***
 *
 * Ce fichier détecte la page courante via un ID unique, appelle l'API Flask,
 * transforme les données avec les fonctions de functions.js, et injecte le
 * résultat dans le DOM. Vous n'avez rien à modifier ici.
 */

const API = "http://localhost:5000/api";

async function api(path, options = {}) {
    const r = await fetch(`${API}${path}`, options);
    if (!r.ok) {
        const err = await r.json().catch(() => ({}));
        throw new Error(err.erreur || `Erreur ${r.status}`);
    }
    return r.json();
}

// ==== SESSION CLIENT (localStorage) ====
const SESSION_KEY = "bracovoit_session";

function getSession() {
    try { return JSON.parse(localStorage.getItem(SESSION_KEY)); }
    catch { return null; }
}

function setSession(compte) {
    localStorage.setItem(SESSION_KEY, JSON.stringify(compte));
}

function clearSession() {
    localStorage.removeItem(SESSION_KEY);
}

function initNavSession() {
    const el = document.getElementById("nav-session");
    if (!el) return;
    const session = getSession();
    if (session) {
        el.innerHTML = `Bonjour ${session.nom} <button id="btn-deconnexion">Déconnexion</button>`;
        document.getElementById("btn-deconnexion").addEventListener("click", () => {
            clearSession();
            window.location.reload();
        });
    } else {
        el.innerHTML = `<a href="../login/login.html">Se connecter</a> <a href="../inscription/inscription.html">S'inscrire</a>`;
    }
}

// ==== ROUTAGE PAR PAGE ====
document.addEventListener("DOMContentLoaded", () => {
    initNavSession();
    if (document.getElementById("page-accueil"))       initAccueil();
    if (document.getElementById("page-recherche"))     initRecherche();
    if (document.getElementById("page-trajet"))        initTrajet();
    if (document.getElementById("page-proposer"))      initProposer();
    if (document.getElementById("page-mes-trajets"))   initMesTrajets();
    if (document.getElementById("page-dashboard"))     initDashboard();
    if (document.getElementById("page-confirmation"))  initConfirmation();
    if (document.getElementById("page-inscription"))   initInscription();
    if (document.getElementById("page-login"))         initLogin();
});

// ==== PAGE ACCUEIL ====
async function initAccueil() {
    let trajets, dashboard;
    try {
        trajets = await api("/trajets");
    } catch (e) { showError(e.message); }

    try {
        dashboard = await api("/dashboard");
    } catch (e) { showError(e.message); }

    if (trajets) {
        try {
            const aujourdhui = new Date().toISOString().split("T")[0];
            setText("nb-trajets-aujourdhui", compterTrajetsAujourdhui(trajets, aujourdhui));
        } catch (e) { console.error("nb-trajets-aujourdhui :", e); }
    }

    if (dashboard) {
        try {
            setText("quartier-principal", formaterQuartierPrincipal(dashboard.trajets_par_quartier));
        } catch (e) { console.error("quartier-principal :", e); }
        try {
            setText("nb-conducteurs", dashboard.total_conducteurs_actifs);
            setText("note-moyenne", dashboard.note_moyenne_conducteurs + " / 5");
        } catch (e) { console.error("cartes dashboard :", e); }
    }
}

// ==== PAGE RECHERCHE ====
async function initRecherche() {
    const btnRecherche = document.getElementById("btn-rechercher");
    const inputMotCle = document.getElementById("champ-recherche");
    const selectDepart = document.getElementById("filtre-depart");
    const container = document.getElementById("liste-trajets");

    async function raffraichir() {
        try {
            const depart = selectDepart ? selectDepart.value : "";
            const motCle = inputMotCle ? inputMotCle.value.trim() : "";
            let trajets = await api("/trajets" + (depart ? `?depart=${depart}` : ""));
            trajets = filtrerParQuartierDepart(trajets, depart);
            trajets = rechercherParMotCle(trajets, motCle);

            if (trajets.length === 0) {
                container.innerHTML = `<p class="aucun-resultat">Aucun trajet trouvé.</p>`;
                return;
            }
            container.innerHTML = trajets.map(t => {
                const badge = getBadgeDisponibilite(t.places_restantes);
                return `<article class="carte-trajet">
                    <h3>${t.quartier_depart} → ${t.quartier_arrivee}</h3>
                    <p class="heure">${formaterHeure(t.heure)}</p>
                    <p class="conducteur">Conducteur : ${t.conducteur.nom} (${t.conducteur.note}/5)</p>
                    <p class="prix">${formaterPrix(t.prix_place)}</p>
                    <span class="badge ${badge.classe}">${badge.libelle}</span>
                    <a href="../trajet/trajet.html?id=${t.id}" class="btn-voir">Voir le trajet</a>
                </article>`;
            }).join("");
        } catch (e) { showError(e.message); }
    }

    if (selectDepart) {
        try {
            const quartiers = await api("/quartiers");
            selectDepart.innerHTML = `<option value="">Tous les quartiers</option>` +
                quartiers.map(q => `<option value="${q}">${q}</option>`).join("");
        } catch (e) { showError(e.message); }
    }

    if (btnRecherche) btnRecherche.addEventListener("click", raffraichir);
    if (selectDepart) selectDepart.addEventListener("change", raffraichir);
    raffraichir();
}

// ==== PAGE DÉTAIL TRAJET ====
async function initTrajet() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");
    if (!id) return showError("Aucun trajet spécifié");

    try {
        const t = await api(`/trajets/${id}`);
        setText("trajet-titre", `${t.quartier_depart} → ${t.quartier_arrivee}`);
        setText("trajet-heure", formaterHeure(t.heure));
        setText("trajet-date", t.date);
        setText("trajet-prix", formaterPrix(t.prix_place));
        setText("trajet-commentaire", t.commentaire || "(aucun commentaire)");
        setText("conducteur-nom", t.conducteur.nom);
        setText("conducteur-vehicule", t.conducteur.vehicule);
        setText("conducteur-note", t.conducteur.note + " / 5");
        setText("conducteur-trajets", t.conducteur.trajets_effectues + " trajets");

        const badge = getBadgeDisponibilite(t.places_restantes);
        const badgeEl = document.getElementById("badge-places");
        if (badgeEl) { badgeEl.textContent = badge.libelle; badgeEl.className = "badge " + badge.classe; }

        const form = document.getElementById("form-reservation");
        const btn = document.getElementById("btn-reserver");
        const errBox = document.getElementById("erreurs-form");
        const inputNom = document.getElementById("r-nom");
        const inputTel = document.getElementById("r-tel");

        const session = getSession();
        if (session && inputNom && inputTel) {
            inputNom.value = session.nom;
            inputTel.value = session.telephone;
        }

        if (btn) btn.disabled = t.places_restantes === 0;

        if (form) {
            form.addEventListener("submit", async (e) => {
                e.preventDefault();
                const nom = inputNom.value.trim();
                const tel = inputTel.value.trim();
                if (!nom || !tel) {
                    if (errBox) {
                        errBox.hidden = false;
                        errBox.innerHTML = "<ul><li>Nom et téléphone requis</li></ul>";
                    }
                    return;
                }
                if (errBox) errBox.hidden = true;
                try {
                    await api("/reservations", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ trajet_id: t.id, passager_nom: nom, passager_tel: tel }),
                    });
                    const msg = formaterMessageConfirmation(nom, t.quartier_depart, t.quartier_arrivee, t.heure);
                    window.location.href = `../confirmation/confirmation.html?msg=${encodeURIComponent(msg)}&tel=${encodeURIComponent(tel)}`;
                } catch (err) { showError(err.message); }
            });
        }
    } catch (e) { showError(e.message); }
}

// ==== PAGE PROPOSER ====
async function initProposer() {
    const form = document.getElementById("form-proposer");
    const selectDepart = document.getElementById("p-depart");
    const selectArrivee = document.getElementById("p-arrivee");
    const errBox = document.getElementById("erreurs-form");

    if (selectDepart && selectArrivee) {
        try {
            const quartiers = await api("/quartiers");
            const opts = quartiers.map(q => `<option value="${q}">${q}</option>`).join("");
            selectDepart.innerHTML = `<option value="">-- Choisir --</option>` + opts;
            selectArrivee.innerHTML = `<option value="">-- Choisir --</option>` + opts;
        } catch (e) { showError(e.message); }
    }

    if (form) {
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            const formulaire = {
                quartier_depart: selectDepart.value,
                quartier_arrivee: selectArrivee.value,
                heure: document.getElementById("p-heure").value,
                places_dispo: document.getElementById("p-places").value,
                prix_place: document.getElementById("p-prix").value,
            };
            const validation = validerFormulaireProposer(formulaire);
            if (!validation.valide) {
                errBox.hidden = false;
                errBox.innerHTML = "<ul>" + validation.erreurs.map(e => `<li>${e}</li>`).join("") + "</ul>";
                return;
            }
            errBox.hidden = true;
            const msg = `Votre proposition ${formulaire.quartier_depart} → ${formulaire.quartier_arrivee} à ${formulaire.heure} a été enregistrée.`;
            window.location.href = `../confirmation/confirmation.html?msg=${encodeURIComponent(msg)}`;
        });
    }
}

// ==== PAGE MES TRAJETS ====
async function initMesTrajets() {
    const inputTel = document.getElementById("mt-tel");
    const btnCharger = document.getElementById("btn-charger-mestrajets");
    const filtreStatut = document.getElementById("mt-filtre-statut");
    const container = document.getElementById("mt-liste");
    const totalEl = document.getElementById("mt-total");

    async function charger() {
        const tel = inputTel.value.trim();
        if (!tel) return;
        try {
            let reservations = await api(`/reservations/${tel}`);
            reservations = filtrerReservationsParStatut(reservations, filtreStatut ? filtreStatut.value : "");
            if (reservations.length === 0) {
                container.innerHTML = `<p>Aucune réservation.</p>`;
                totalEl.textContent = formaterPrix(0);
                return;
            }
            container.innerHTML = reservations.map(r => `
                <article class="carte-reservation">
                    <h3>${r.trajet.quartier_depart} → ${r.trajet.quartier_arrivee}</h3>
                    <p>Date : ${r.trajet.date} à ${formaterHeure(r.trajet.heure)}</p>
                    <p>Conducteur : ${r.conducteur.nom}</p>
                    <p>Prix : ${formaterPrix(r.trajet.prix_place)}</p>
                    <span class="statut statut-${r.statut}">${r.statut}</span>
                </article>
            `).join("");
            totalEl.textContent = formaterPrix(calculerTotalDepenseParPassager(reservations));
        } catch (e) { showError(e.message); }
    }

    if (btnCharger) btnCharger.addEventListener("click", charger);
    if (filtreStatut) filtreStatut.addEventListener("change", charger);

    const session = getSession();
    if (session) {
        inputTel.value = session.telephone;
        charger();
    }
}

// ==== PAGE DASHBOARD ====
async function initDashboard() {
    let d;
    try {
        d = await api("/dashboard");
    } catch (e) { showError(e.message); return; }

    try {
        setText("d-trajets", d.total_trajets_disponibles);
        setText("d-conducteurs", d.total_conducteurs_actifs);
        setText("d-reservations", d.total_reservations_actives);
        setText("d-note", d.note_moyenne_conducteurs + " / 5");
        setText("d-taux-annulation", d.taux_annulation + " %");
    } catch (e) { console.error("cartes indicateurs :", e); }

    try {
        const topCond = document.getElementById("d-top-conducteurs");
        if (topCond) {
            topCond.innerHTML = d.top_conducteurs.map((c, i) =>
                `<li><strong>#${i + 1}</strong> ${c.nom} — ${c.note}/5 (${c.trajets_effectues} trajets)</li>`
            ).join("");
        }
    } catch (e) { console.error("top conducteurs :", e); }

    try {
        const trajetTop = document.getElementById("d-trajet-top");
        if (trajetTop && d.trajet_le_plus_reserve) {
            trajetTop.textContent = `${d.trajet_le_plus_reserve.trajet_libelle} (${d.trajet_le_plus_reserve.nombre_reservations} réservations)`;
        }
    } catch (e) { console.error("trajet vedette :", e); }

    try {
        const trajQuartier = document.getElementById("d-trajets-par-quartier");
        if (trajQuartier) {
            trajQuartier.innerHTML = Object.entries(d.trajets_par_quartier)
                .sort((a, b) => b[1] - a[1])
                .map(([q, n]) => `<tr><td>${q}</td><td>${n}</td><td>${formaterPrix(d.prix_moyen_par_quartier[q] || 0)}</td></tr>`).join("");
        }
    } catch (e) { console.error("tableau par quartier :", e); }
}

// ==== PAGE CONFIRMATION ====
function initConfirmation() {
    const params = new URLSearchParams(window.location.search);
    const msg = params.get("msg");
    const tel = params.get("tel");
    if (msg) setText("confirmation-message", decodeURIComponent(msg));
    if (tel) {
        const lien = document.getElementById("lien-mes-trajets");
        if (lien) lien.href = `../mes-trajets/mes-trajets.html?tel=${tel}`;
    }
}

// ==== PAGE INSCRIPTION ====
function initInscription() {
    const form = document.getElementById("form-inscription");
    const errBox = document.getElementById("erreurs-form");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formulaire = {
            nom: document.getElementById("i-nom").value,
            telephone: document.getElementById("i-telephone").value,
            mot_de_passe: document.getElementById("i-mot-de-passe").value,
        };
        const validation = validerFormulaireInscription(formulaire);
        if (!validation.valide) {
            errBox.hidden = false;
            errBox.innerHTML = "<ul>" + validation.erreurs.map(e => `<li>${e}</li>`).join("") + "</ul>";
            return;
        }
        errBox.hidden = true;
        try {
            await api("/inscription", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formulaire),
            });
            window.location.href = "../login/login.html";
        } catch (err) { showError(err.message); }
    });
}

// ==== PAGE LOGIN ====
function initLogin() {
    const form = document.getElementById("form-login");
    const errBox = document.getElementById("erreurs-form");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formulaire = {
            telephone: document.getElementById("l-telephone").value,
            mot_de_passe: document.getElementById("l-mot-de-passe").value,
        };
        const validation = validerFormulaireLogin(formulaire);
        if (!validation.valide) {
            errBox.hidden = false;
            errBox.innerHTML = "<ul>" + validation.erreurs.map(e => `<li>${e}</li>`).join("") + "</ul>";
            return;
        }
        errBox.hidden = true;
        try {
            const result = await api("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formulaire),
            });
            setSession(result.compte);
            window.location.href = "../accueil/index.html";
        } catch (err) { showError(err.message); }
    });
}

// ==== HELPERS ====
function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
}

function showError(msg) {
    const errEl = document.getElementById("erreur-globale");
    if (errEl) {
        errEl.textContent = "Erreur : " + msg;
        errEl.hidden = false;
    } else {
        console.error("Erreur:", msg);
    }
}
