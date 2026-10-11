/* Fiche véhicule : vehicule.html?id=<id> */
(function () {
  var PL = window.PL, e = PL.esc;
  var root = document.getElementById('fiche');
  if (!root) return;
  var id = PL.params().get('id');
  var v = PL.byId(id) || (id ? null : PL.vehicles[0]);

  var ARROW = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 10h12M11 5l5 5-5 5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var CHECK = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 10.5l4 4 8-9" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var PHONE = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 2.5h3l1.5 4-2 1.3a9 9 0 0 0 4.7 4.7l1.3-2 4 1.5v3a2 2 0 0 1-2 2A14.5 14.5 0 0 1 3 4.5a2 2 0 0 1 2-2z" stroke-linejoin="round"/></svg>';

  if (!v) {
    root.innerHTML = '<section class="notfound"><div class="wrap"><h1 class="h2">Ce véhicule n\'est plus en ligne.</h1>' +
      '<p class="lead" style="margin-top:20px">Il a peut-être été vendu. Parcourez le stock actuel ou demandez à Pierre-Lou de vous trouver un modèle équivalent.</p>' +
      '<p style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="vehicules.html">Voir les véhicules ' + ARROW + '</a>' +
      '<a class="btn btn--ghost" href="contact.html?demande=recherche">Lancer une recherche</a></p></div></section>';
    return;
  }

  document.title = v.marque + ' ' + v.modele + ' ' + v.annee + ' · Pierre-Lou Automobiles';

  var VIEWS = ['Vue 3/4 avant', 'Profil', 'Vue 3/4 arrière', 'Intérieur, poste de conduite', 'Sièges arrière', 'Coffre'];
  var slides = VIEWS.map(function (label, i) {
    return '<div class="ph' + (i === 0 ? ' is-active' : '') + '" data-ph="' + (i < 3 ? 'car' : 'photo') + '" data-label="' + label + '" data-hint="' + v.id + '-' + (i + 1) + '.jpg" data-src="' + PL.photo(v, i + 1) + '"></div>';
  }).join('');
  var thumbs = VIEWS.map(function (label, i) {
    return '<button type="button" aria-label="Photo ' + (i + 1) + ' : ' + label + '" aria-current="' + (i === 0) + '"><div class="ph" data-ph="' + (i < 3 ? 'car' : 'photo') + '" data-src="' + PL.photo(v, i + 1) + '"></div></button>';
  }).join('');

  var specs = [
    ['Année', v.annee], ['Kilométrage', PL.fmtKm(v.km)], ['Énergie', v.carburant],
    ['Boîte', v.boite], ['Puissance', v.puissance + ' ch'], ['Couleur', v.couleur],
    ['Portes / places', v.portes + ' / ' + v.places], ['Crit\'Air', v.critair === 0 ? 'Zéro émission' : v.critair], ['Garantie', v.garantie + ' mois']
  ].map(function (s) { return '<div class="spec"><small>' + s[0] + '</small><strong>' + e(String(s[1])) + '</strong></div>'; }).join('');

  var similar = PL.vehicles.filter(function (x) { return x.id !== v.id; })
    .sort(function (a, b) { return Math.abs(a.prix - v.prix) - Math.abs(b.prix - v.prix); }).slice(0, 3);

  var tag = v.statut !== 'Disponible' ? '<span class="tag tag--' + (v.statut === 'Réservé' ? 'held' : 'new') + '">' + e(v.statut) + '</span>' : '';

  root.innerHTML =
    '<section class="fiche"><div class="wrap">' +
      '<nav class="crumbs" aria-label="Fil d\'Ariane"><a href="index.html">Accueil</a><span aria-hidden="true">/</span><a href="vehicules.html">Véhicules</a><span aria-hidden="true">/</span><span>' + e(v.marque + ' ' + v.modele) + '</span></nav>' +
      '<div class="fiche-grid">' +
        '<div>' +
          '<div class="gallery-main wipe" data-hero>' + slides +
            '<button class="gal-nav gal-prev" type="button" aria-label="Photo précédente"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 10H4M9 5l-5 5 5 5" stroke-linecap="round" stroke-linejoin="round"/></svg></button>' +
            '<button class="gal-nav gal-next" type="button" aria-label="Photo suivante">' + ARROW + '</button>' +
            '<span class="gal-count" aria-live="polite">1 / 6</span>' +
          '</div>' +
          '<div class="thumbs">' + thumbs + '</div>' +
          '<div class="specs">' + specs + '</div>' +
          '<div class="equip"><h2>Équipements principaux</h2><ul>' + v.options.map(function (o) { return '<li>' + CHECK + e(o) + '</li>'; }).join('') + '</ul></div>' +
          '<div class="promise">' +
            '<div><b>Garantie ' + v.garantie + ' mois</b>Moteur, boîte et pièces principales.</div>' +
            '<div><b>Contrôle technique OK</b>Réalisé il y a moins de 6 mois.</div>' +
            '<div><b>Carte grise faite</b>Vous repartez avec le véhicule à votre nom.</div>' +
          '</div>' +
          '<div class="finance" id="finance"><h2>Simuler une mensualité</h2>' +
            '<div class="finance-grid"><div>' +
              '<div class="f-group"><label class="f-label" for="apport">Apport <output id="apport-out"></output></label><input type="range" id="apport" min="0" max="' + Math.round(v.prix * .5 / 500) * 500 + '" step="500" value="' + Math.round(v.prix * .1 / 500) * 500 + '"></div>' +
              '<fieldset class="f-group" style="border:0;padding:0;margin:22px 0 0"><legend class="f-label">Durée</legend><div class="chips dur">' +
                [24, 36, 48, 60, 72].map(function (m) { return '<label class="chip"><input type="radio" name="duree" value="' + m + '"' + (m === 60 ? ' checked' : '') + '>' + m + ' mois</label>'; }).join('') +
              '</div></fieldset>' +
            '</div>' +
            '<div class="finance-result"><div class="mth"><span id="mth">0</span><small> €/mois</small></div>' +
            '<p>TAEG fixe indicatif de ' + (PL.TAUX * 100).toLocaleString('fr-FR') + ' %, hors assurance. Exemple non contractuel, sous réserve d\'acceptation.</p></div>' +
          '</div></div>' +
        '</div>' +
        '<aside class="fiche-side">' +
          '<div class="fiche-title">' +
            '<div class="fiche-meta"><span class="plate-ref">' + e(v.ref) + '</span>' + tag + '</div>' +
            '<h1 class="lines" data-hero><span class="ln"><span>' + e(v.marque) + '</span></span><span class="ln"><span>' + e(v.modele) + '</span></span></h1>' +
            '<p>' + e(v.version) + '</p>' +
          '</div>' +
          '<div class="price-card">' +
            '<div class="price-big" id="price">' + PL.fmtPrice(v.prix) + '</div>' +
            '<p class="sub">Préparation, garantie et carte grise comprises. Ou dès <a class="link" href="#finance" style="color:inherit" id="mth-link"></a>.</p>' +
            '<div class="btns">' +
              '<a class="btn btn--block magnetic" href="contact.html?demande=achat&vehicule=' + e(v.id) + '&essai=1">Réserver un essai ' + ARROW + '</a>' +
              '<a class="btn btn--ghost btn--block" href="tel:+33299000000">' + PHONE + '02 99 00 00 00</a>' +
              '<a class="btn btn--ghost btn--block" href="contact.html?demande=reprise&vehicule=' + e(v.id) + '">Proposer ma voiture en reprise</a>' +
            '</div>' +
          '</div>' +
          '<p style="font-size:14px;color:var(--slate);margin:0">Référence ' + e(v.ref) + '. Visible au garage sur rendez-vous. <span data-open></span></p>' +
        '</aside>' +
      '</div>' +
      '<section class="similar"><div class="sec-head" style="margin-bottom:28px"><h2>Dans le même budget</h2><a class="link" href="vehicules.html">Tout le stock</a></div>' +
        '<div class="similar-grid">' + similar.map(PL.cardHTML).join('') + '</div></section>' +
    '</div></section>' +
    '<div class="mobile-buy" id="mobile-buy"><strong>' + PL.fmtPrice(v.prix) + '</strong><a class="btn btn--sm" href="contact.html?demande=achat&vehicule=' + e(v.id) + '&essai=1">Réserver un essai</a></div>';

  // statut d'ouverture dans le contenu injecté
  root.querySelectorAll('[data-open]').forEach(function (el) {
    var s = PL.openStatus(); el.textContent = s.text; el.classList.add('open-status', s.open ? 'is-open' : 'is-closed');
  });
  PL.initPh(root);
  PL.observeReveals(root);
  PL.magnetic(root);
  PL.tilt(root);
  PL.ready(function () { root.querySelectorAll('[data-hero]').forEach(function (el) { el.classList.add('in'); }); });

  /* ---------- Galerie ---------- */
  var slidesEl = root.querySelectorAll('.gallery-main .ph');
  var thumbBtns = root.querySelectorAll('.thumbs button');
  var count = root.querySelector('.gal-count');
  var cur = 0;
  function go(i) {
    cur = (i + slidesEl.length) % slidesEl.length;
    slidesEl.forEach(function (s, k) { s.classList.toggle('is-active', k === cur); if (k === cur) s.classList.add('is-drawn'); });
    thumbBtns.forEach(function (b, k) { b.setAttribute('aria-current', k === cur); });
    count.textContent = (cur + 1) + ' / ' + slidesEl.length;
  }
  thumbBtns.forEach(function (b, k) { b.addEventListener('click', function () { go(k); }); });
  root.querySelector('.gal-prev').addEventListener('click', function () { go(cur - 1); });
  root.querySelector('.gal-next').addEventListener('click', function () { go(cur + 1); });
  var gm = root.querySelector('.gallery-main');
  gm.tabIndex = 0;
  gm.setAttribute('aria-label', 'Galerie photo, flèches gauche et droite pour naviguer');
  gm.addEventListener('keydown', function (ev) {
    if (ev.key === 'ArrowLeft') go(cur - 1);
    if (ev.key === 'ArrowRight') go(cur + 1);
  });
  // balayage tactile
  var sx = null;
  gm.addEventListener('touchstart', function (ev) { sx = ev.touches[0].clientX; }, { passive: true });
  gm.addEventListener('touchend', function (ev) {
    if (sx === null) return;
    var dx = ev.changedTouches[0].clientX - sx;
    if (Math.abs(dx) > 40) go(cur + (dx < 0 ? 1 : -1));
    sx = null;
  });

  /* ---------- Simulateur ---------- */
  var apport = document.getElementById('apport');
  var mthEl = document.getElementById('mth');
  var shown = 0;
  function calc() {
    var a = +apport.value;
    var mois = +root.querySelector('input[name="duree"]:checked').value;
    var m = Math.round(PL.monthly(v.prix - a, mois));
    document.getElementById('apport-out').textContent = PL.fmtPrice(a);
    apport.style.setProperty('--p', (a / apport.max * 100) + '%');
    document.getElementById('mth-link').textContent = m + ' €/mois sur ' + mois + ' mois';
    var from = shown, t0 = performance.now();
    shown = m;
    if (PL.reduced) { mthEl.textContent = m; return; }
    (function f(now) {
      var p = Math.min(1, (now - t0) / 450), k = 1 - Math.pow(1 - p, 3);
      mthEl.textContent = Math.round(from + (m - from) * k);
      if (p < 1) requestAnimationFrame(f);
    })(t0);
  }
  apport.addEventListener('input', calc);
  root.querySelectorAll('input[name="duree"]').forEach(function (r) { r.addEventListener('change', calc); });
  calc();

  /* ---------- Barre d'achat mobile ---------- */
  var bar = document.getElementById('mobile-buy');
  var priceCard = root.querySelector('.price-card');
  new IntersectionObserver(function (en) {
    bar.classList.toggle('is-on', !en[0].isIntersecting && en[0].boundingClientRect.top < 0);
  }).observe(priceCard);
})();
