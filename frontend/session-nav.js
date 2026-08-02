/*
 * Adaptateur visuel de la session.
 * main.js reste intact : ce fichier enrichit uniquement #nav-session.
 */
(function initSessionNavigation() {
  const SESSION_KEY = "bracovoit_session";
  const PROFILE_IMAGE = "../assets/images/portrait-diane.webp";

  function readSession() {
    try {
      return JSON.parse(localStorage.getItem(SESSION_KEY));
    } catch {
      return null;
    }
  }

  function createLink(label, href, className) {
    const link = document.createElement("a");
    link.className = className;
    link.href = href;
    link.textContent = label;
    return link;
  }

  function createAvatar(className) {
    const image = document.createElement("img");
    image.className = className;
    image.src = PROFILE_IMAGE;
    image.alt = "";
    image.width = 80;
    image.height = 80;
    return image;
  }

  function renderGuestNavigation(container) {
    const actions = document.createElement("div");
    actions.className = "session-auth";
    actions.append(
      createLink("Se connecter", "../login/login.html", "session-auth__link"),
      createLink("S'inscrire", "../inscription/inscription.html", "session-auth__link session-auth__link--primary"),
    );
    container.replaceChildren(actions);
  }

  function renderProfileNavigation(container, session) {
    const menu = document.createElement("details");
    menu.className = "session-menu";

    const trigger = document.createElement("summary");
    trigger.className = "session-menu__trigger";
    trigger.setAttribute("aria-label", `Ouvrir le menu du compte de ${session.nom}`);

    const triggerIdentity = document.createElement("span");
    triggerIdentity.className = "session-menu__identity";
    const triggerName = document.createElement("strong");
    triggerName.textContent = session.nom;
    const triggerPhone = document.createElement("span");
    triggerPhone.textContent = session.telephone;
    triggerIdentity.append(triggerName, triggerPhone);

    const chevron = document.createElement("i");
    chevron.className = "ph ph-caret-down session-menu__chevron";
    chevron.setAttribute("aria-hidden", "true");
    trigger.append(createAvatar("session-menu__avatar"), triggerIdentity, chevron);

    const panel = document.createElement("div");
    panel.className = "session-menu__panel";

    const profile = document.createElement("div");
    profile.className = "session-menu__profile";
    const profileIdentity = document.createElement("span");
    profileIdentity.className = "session-menu__profile-copy";
    const profileName = document.createElement("strong");
    profileName.textContent = session.nom;
    const profilePhone = document.createElement("span");
    profilePhone.textContent = session.telephone;
    profileIdentity.append(profileName, profilePhone);
    profile.append(createAvatar("session-menu__avatar session-menu__avatar--large"), profileIdentity);

    const navigation = document.createElement("nav");
    navigation.className = "session-menu__links";
    navigation.setAttribute("aria-label", "Navigation du compte");
    navigation.append(
      createLink("Mes trajets", "../mes-trajets/mes-trajets.html", "session-menu__link"),
      createLink("Proposer un trajet", "../proposer/proposer.html", "session-menu__link"),
    );

    const logout = document.createElement("button");
    logout.id = "btn-deconnexion";
    logout.className = "session-menu__logout";
    logout.type = "button";
    const logoutIcon = document.createElement("i");
    logoutIcon.className = "ph ph-sign-out";
    logoutIcon.setAttribute("aria-hidden", "true");
    const logoutLabel = document.createElement("span");
    logoutLabel.textContent = "Se déconnecter";
    logout.append(logoutIcon, logoutLabel);
    logout.addEventListener("click", () => {
      localStorage.removeItem(SESSION_KEY);
      window.location.reload();
    });

    panel.append(profile, navigation, logout);
    menu.append(trigger, panel);
    container.replaceChildren(menu);

    document.addEventListener("click", (event) => {
      if (!menu.contains(event.target)) menu.open = false;
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") menu.open = false;
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("nav-session");
    if (!container) return;

    const session = readSession();
    if (session?.nom && session?.telephone) {
      renderProfileNavigation(container, session);
      return;
    }
    renderGuestNavigation(container);
  });
})();
