/* ==========================================================================
   Stock de véhicules.
   En ligne, le stock vient de content/vehicules.json, que Pierre-Lou modifie
   depuis l'espace d'administration (/admin). La liste ci-dessous ne sert
   que de secours (ouverture du site en local, fichier absent).

   EXEMPLES pour la maquette.
   À remplacer par le stock réel de Pierre-Lou.

   Photos : déposer les fichiers dans assets/photos/vehicules/
   en les nommant  <id>-1.jpg, <id>-2.jpg … <id>-6.jpg
   (ex. peugeot-208-2021-1.jpg). La photo n°1 sert de vignette.
   Tant qu'un fichier est absent, un emplacement photo s'affiche à la place.
   ========================================================================== */

window.PL = window.PL || {};

PL.vehicles = [
  {
    id: 'peugeot-208-2021', ref: 'PL-001', marque: 'Peugeot', modele: '208',
    version: '1.2 PureTech 100 Allure', annee: 2021, km: 32400, carburant: 'Essence',
    boite: 'Manuelle', puissance: 100, prix: 15490, couleur: 'Gris Artense', portes: 5,
    places: 5, critair: 1, garantie: 12, statut: 'Nouveauté', vitrine: true,
    options: ['Écran tactile 10"', 'Apple CarPlay / Android Auto', 'Radar de recul', 'Climatisation automatique', 'Régulateur de vitesse', 'Jantes alliage 16"']
  },
  {
    id: 'toyota-yaris-2022', ref: 'PL-002', marque: 'Toyota', modele: 'Yaris',
    version: 'Hybride 116h Design', annee: 2022, km: 18900, carburant: 'Hybride',
    boite: 'Automatique', puissance: 116, prix: 19490, couleur: 'Blanc pur', portes: 5,
    places: 5, critair: 1, garantie: 24, statut: 'Disponible', vitrine: true,
    options: ['Caméra de recul', 'Toyota Safety Sense', 'Sièges chauffants', 'Apple CarPlay / Android Auto', 'Clim. automatique']
  },
  {
    id: 'dacia-duster-2021', ref: 'PL-003', marque: 'Dacia', modele: 'Duster',
    version: 'TCe 130 Prestige 4x2', annee: 2021, km: 36700, carburant: 'Essence',
    boite: 'Manuelle', puissance: 130, prix: 16990, couleur: 'Orange Atacama', portes: 5,
    places: 5, critair: 1, garantie: 12, statut: 'Disponible', vitrine: true,
    options: ['Caméra multivues', 'Navigation', 'Démarrage sans clé', 'Barres de toit', 'Jantes 17"']
  },
  {
    id: 'tesla-model3-2021', ref: 'PL-004', marque: 'Tesla', modele: 'Model 3',
    version: 'Standard Range Plus', annee: 2021, km: 54000, carburant: 'Électrique',
    boite: 'Automatique', puissance: 283, prix: 27900, couleur: 'Gris nuit', portes: 4,
    places: 5, critair: 0, garantie: 12, statut: 'Réservé', vitrine: true,
    options: ['Autopilot', 'Toit vitré', 'Sièges chauffants AV/AR', 'Caméra 360°', 'Charge rapide']
  },
  {
    id: 'peugeot-3008-2020', ref: 'PL-005', marque: 'Peugeot', modele: '3008',
    version: '1.5 BlueHDi 130 EAT8 GT Line', annee: 2020, km: 69800, carburant: 'Diesel',
    boite: 'Automatique', puissance: 130, prix: 22490, couleur: 'Bleu Célèbes', portes: 5,
    places: 5, critair: 2, garantie: 12, statut: 'Disponible', vitrine: true,
    options: ['i-Cockpit 12,3"', 'Navigation 3D', 'Hayon électrique', 'Full LED', 'Aide au stationnement AV/AR', 'Jantes 18"']
  },
  {
    id: 'mini-cooper-2019', ref: 'PL-006', marque: 'Mini', modele: 'Cooper',
    version: '136 ch Chili, 3 portes', annee: 2019, km: 47300, carburant: 'Essence',
    boite: 'Manuelle', puissance: 136, prix: 17490, couleur: 'British Racing Green', portes: 3,
    places: 4, critair: 1, garantie: 12, statut: 'Nouveauté', vitrine: true,
    options: ['Toit contrasté', 'Sièges sport', 'Phares LED', 'Navigation', 'Mode Sport']
  },
  {
    id: 'renault-clio-2020', ref: 'PL-007', marque: 'Renault', modele: 'Clio V',
    version: 'TCe 90 Intens', annee: 2020, km: 41200, carburant: 'Essence',
    boite: 'Manuelle', puissance: 90, prix: 13290, couleur: 'Bleu Iron', portes: 5,
    places: 5, critair: 1, garantie: 12, statut: 'Disponible', vitrine: false,
    options: ['Écran 9,3"', 'Caméra de recul', 'Carte mains libres', 'Clim. automatique']
  },
  {
    id: 'vw-golf-2019', ref: 'PL-008', marque: 'Volkswagen', modele: 'Golf 7',
    version: '2.0 TDI 150 DSG7 Carat', annee: 2019, km: 78500, carburant: 'Diesel',
    boite: 'Automatique', puissance: 150, prix: 19990, couleur: 'Noir intense', portes: 5,
    places: 5, critair: 2, garantie: 12, statut: 'Disponible', vitrine: false,
    options: ['Active Info Display', 'Régulateur adaptatif', 'Sellerie cuir', 'Navigation Discover', 'Park Assist']
  },
  {
    id: 'citroen-c3-2019', ref: 'PL-009', marque: 'Citroën', modele: 'C3',
    version: 'PureTech 82 Feel', annee: 2019, km: 61000, carburant: 'Essence',
    boite: 'Manuelle', puissance: 82, prix: 9990, couleur: 'Rouge Aden', portes: 5,
    places: 5, critair: 1, garantie: 6, statut: 'Disponible', vitrine: false,
    options: ['Airbump', 'Écran tactile 7"', 'Régulateur de vitesse', 'Climatisation']
  },
  {
    id: 'audi-a3-2018', ref: 'PL-010', marque: 'Audi', modele: 'A3 Sportback',
    version: '1.5 TFSI 150 S tronic S line', annee: 2018, km: 84200, carburant: 'Essence',
    boite: 'Automatique', puissance: 150, prix: 20900, couleur: 'Gris Daytona', portes: 5,
    places: 5, critair: 1, garantie: 12, statut: 'Disponible', vitrine: false,
    options: ['Virtual Cockpit', 'Pack S line', 'Phares Xénon', 'Navigation MMI', 'Sièges sport']
  },
  {
    id: 'renault-captur-2022', ref: 'PL-011', marque: 'Renault', modele: 'Captur',
    version: 'E-Tech hybride rechargeable 160 Intens', annee: 2022, km: 24100, carburant: 'Hybride',
    boite: 'Automatique', puissance: 160, prix: 23990, couleur: 'Blanc nacré', portes: 5,
    places: 5, critair: 1, garantie: 24, statut: 'Disponible', vitrine: false,
    options: ['Câble de recharge', 'Écran 9,3" vertical', 'Caméra 360°', 'Banquette coulissante']
  },
  {
    id: 'skoda-octavia-2020', ref: 'PL-012', marque: 'Skoda', modele: 'Octavia Combi',
    version: '2.0 TDI 150 DSG7 Style', annee: 2020, km: 92000, carburant: 'Diesel',
    boite: 'Automatique', puissance: 150, prix: 18990, couleur: 'Gris Quartz', portes: 5,
    places: 5, critair: 2, garantie: 12, statut: 'Disponible', vitrine: false,
    options: ['Coffre 640 L', 'Virtual Cockpit', 'Attelage', 'Régulateur adaptatif', 'Hayon électrique']
  }
];

/* ---------- Helpers partagés ---------- */

// Séparateur de milliers : espace insécable classique (l'espace fine n'existe pas dans la police)
PL.fmtNum = function (n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, '\u00a0'); };
PL.fmtPrice = function (n) { return PL.fmtNum(n) + '\u00a0€'; };
PL.fmtKm = function (n) { return PL.fmtNum(n) + '\u00a0km'; };
PL.photo = function (v, i) {
  var p = v.photos && v.photos[(i || 1) - 1];
  if (p) return String(p).replace(/^\//, '');
  return 'assets/photos/vehicules/' + v.id + '-' + (i || 1) + '.jpg';
};
PL.byId = function (id) {
  for (var i = 0; i < PL.vehicles.length; i++) if (PL.vehicles[i].id === id) return PL.vehicles[i];
  return null;
};

/* ---------- Données gérées depuis /admin ---------- */
PL.slug = function (s) {
  return String(s).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
};
PL.photoMap = {};
PL.setVehicles = function (list) {
  var seen = {};
  PL.vehicles = list.filter(function (v) { return v && v.marque && v.statut !== 'Vendu'; }).map(function (v, i) {
    var id = PL.slug(v.marque + '-' + v.modele + '-' + v.annee), base = id, n = 2;
    while (seen[id]) id = base + '-' + n++;
    seen[id] = true;
    return {
      id: id, ref: v.ref || 'PL-' + ('00' + (i + 1)).slice(-3),
      marque: v.marque, modele: v.modele || '', version: v.version || '',
      annee: +v.annee || 0, km: +v.km || 0, prix: +v.prix || 0, puissance: +v.puissance || 0,
      carburant: v.carburant || 'Essence', boite: v.boite || 'Manuelle', couleur: v.couleur || '',
      portes: +v.portes || 5, places: +v.places || 5, critair: v.critair == null ? 1 : +v.critair,
      garantie: +v.garantie || 12, statut: v.statut || 'Disponible', vitrine: !!v.vitrine,
      options: (v.options || []).filter(Boolean),
      photos: (v.photos || []).map(function (p) { return typeof p === 'string' ? p : p && p.image; }).filter(Boolean)
    };
  });
};
(function () {
  function getJSON(url) {
    return fetch(url, { cache: 'no-cache' }).then(function (r) { if (!r.ok) throw new Error(url); return r.json(); });
  }
  var fallback = PL.vehicles;
  PL.dataReady = Promise.all([
    getJSON('content/vehicules.json')
      .then(function (d) { PL.setVehicles(d.vehicules || []); })
      .catch(function () { PL.setVehicles(fallback); }),
    getJSON('content/photos.json')
      .then(function (d) { PL.photoMap = d || {}; })
      .catch(function () {})
  ]);
})();

// Mensualité indicative (crédit classique)
PL.TAUX = 0.059;
PL.monthly = function (capital, mois, taux) {
  if (capital <= 0) return 0;
  var r = (taux == null ? PL.TAUX : taux) / 12;
  return capital * r / (1 - Math.pow(1 + r, -mois));
};

PL.esc = function (s) {
  return String(s).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
};

PL.cardHTML = function (v) {
  var e = PL.esc;
  var badge = v.statut !== 'Disponible'
    ? '<span class="tag tag--' + (v.statut === 'Réservé' ? 'held' : 'new') + '">' + e(v.statut) + '</span>' : '';
  var mens = Math.round(PL.monthly(v.prix * 0.9, 60));
  return '' +
    '<a class="car" href="vehicule.html?id=' + e(v.id) + '" data-cursor="Voir la fiche" data-id="' + e(v.id) + '">' +
      '<div class="car-media">' +
        '<div class="ph" data-ph="car" data-label="Photo principale" data-hint="À ajouter depuis l\'espace Pierre-Lou" data-src="' + PL.photo(v, 1) + '"></div>' +
        badge +
      '</div>' +
      '<div class="car-body">' +
        '<div class="car-head">' +
          '<h3>' + e(v.marque) + ' ' + e(v.modele) + '</h3>' +
          '<span class="plate-ref" aria-label="Référence ' + e(v.ref) + '">' + e(v.ref) + '</span>' +
        '</div>' +
        '<p class="car-version">' + e(v.version) + '</p>' +
        '<ul class="car-specs">' +
          '<li>' + v.annee + '</li><li>' + PL.fmtKm(v.km) + '</li><li>' + e(v.carburant) + '</li><li>' + e(v.boite) + '</li>' +
        '</ul>' +
        '<div class="car-price"><strong>' + PL.fmtPrice(v.prix) + '</strong><span>ou ' + mens + ' €/mois*</span></div>' +
      '</div>' +
    '</a>';
};
