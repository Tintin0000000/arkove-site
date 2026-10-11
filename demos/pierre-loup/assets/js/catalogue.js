/* Catalogue : filtres, tri et réarrangement animé (FLIP) */
(function () {
  var PL = window.PL;
  var V = PL.vehicles;
  var $ = function (id) { return document.getElementById(id); };
  var grid = $('grid');
  if (!grid) return;

  function uniq(key) {
    return V.map(function (v) { return v[key]; }).filter(function (x, i, a) { return a.indexOf(x) === i; });
  }
  var maxPrix = Math.ceil(Math.max.apply(null, V.map(function (v) { return v.prix; })) / 1000) * 1000;
  var minPrix = Math.floor(Math.min.apply(null, V.map(function (v) { return v.prix; })) / 1000) * 1000;
  var maxKm = Math.ceil(Math.max.apply(null, V.map(function (v) { return v.km; })) / 10000) * 10000;

  /* ---------- Construction des contrôles ---------- */
  uniq('marque').sort().forEach(function (m) { $('marque').insertAdjacentHTML('beforeend', '<option>' + PL.esc(m) + '</option>'); });
  uniq('annee').sort().reverse().forEach(function (a) { $('annee').insertAdjacentHTML('beforeend', '<option value="' + a + '">' + a + ' et après</option>'); });
  function chips(id, values) {
    $(id).innerHTML = values.map(function (v) {
      return '<label class="chip"><input type="checkbox" value="' + PL.esc(v) + '">' + PL.esc(v) + '</label>';
    }).join('');
  }
  chips('carburant', ['Essence', 'Diesel', 'Hybride', 'Électrique']);
  chips('boite', ['Manuelle', 'Automatique']);

  var prix = $('prix'), km = $('km');
  prix.min = minPrix; prix.max = maxPrix; prix.value = maxPrix;
  km.min = 10000; km.max = maxKm; km.value = maxKm;

  /* ---------- Cartes (créées une fois, réordonnées ensuite) ---------- */
  grid.innerHTML = V.map(PL.cardHTML).join('') +
    '<div class="empty" id="empty" hidden><p class="h3">Aucun véhicule ne correspond.</p><p>Augmentez le budget ou retirez un filtre pour voir plus de résultats.</p><button class="btn btn--sm" type="button" id="empty-reset">Réinitialiser les filtres</button></div>';
  var cards = {};
  grid.querySelectorAll('.car').forEach(function (el) { cards[el.getAttribute('data-id')] = el; });
  var empty = $('empty');
  PL.initPh(grid);
  PL.tilt(grid);

  /* ---------- État ---------- */
  function checked(id) {
    return Array.prototype.map.call($(id).querySelectorAll('input:checked'), function (i) { return i.value; });
  }
  function state() {
    return {
      q: $('q').value.trim().toLowerCase(),
      marque: $('marque').value,
      carburant: checked('carburant'),
      boite: checked('boite'),
      prix: +prix.value,
      km: +km.value,
      annee: +$('annee').value || 0,
      sort: $('sort').value
    };
  }

  function norm(s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }

  function filtered(s) {
    var q = norm(s.q);
    var out = V.filter(function (v) {
      if (q && norm([v.marque, v.modele, v.version, v.couleur, v.carburant].join(' ')).indexOf(q) < 0) return false;
      if (s.marque && v.marque !== s.marque) return false;
      if (s.carburant.length && s.carburant.indexOf(v.carburant) < 0) return false;
      if (s.boite.length && s.boite.indexOf(v.boite) < 0) return false;
      if (v.prix > s.prix) return false;
      if (v.km > s.km) return false;
      if (v.annee < s.annee) return false;
      return true;
    });
    var by = {
      'prix-asc': function (a, b) { return a.prix - b.prix; },
      'prix-desc': function (a, b) { return b.prix - a.prix; },
      'km-asc': function (a, b) { return a.km - b.km; },
      'annee-desc': function (a, b) { return b.annee - a.annee || a.km - b.km; }
    }[s.sort];
    return by ? out.slice().sort(by) : out;
  }

  /* ---------- Rendu + animation FLIP ---------- */
  var countEl = $('count'), lastCount = V.length;
  function render(animate) {
    var s = state();
    var list = filtered(s);
    var first = {};
    if (animate && !PL.reduced) {
      Object.keys(cards).forEach(function (id) {
        if (!cards[id].hidden) first[id] = cards[id].getBoundingClientRect();
      });
    }
    var visible = {};
    list.forEach(function (v) { visible[v.id] = true; grid.insertBefore(cards[v.id], empty); });
    Object.keys(cards).forEach(function (id) { cards[id].hidden = !visible[id]; });
    empty.hidden = list.length > 0;

    if (animate && !PL.reduced) {
      list.forEach(function (v, i) {
        var el = cards[v.id], last = el.getBoundingClientRect(), f = first[v.id];
        if (f) {
          var dx = f.left - last.left, dy = f.top - last.top;
          if (dx || dy) el.animate([{ transform: 'translate(' + dx + 'px,' + dy + 'px)' }, { transform: 'none' }],
            { duration: 650, easing: 'cubic-bezier(.16,1,.3,1)' });
        } else {
          el.animate([{ opacity: 0, transform: 'translateY(30px) scale(.96)' }, { opacity: 1, transform: 'none' }],
            { duration: 600, delay: Math.min(i, 6) * 40, easing: 'cubic-bezier(.16,1,.3,1)', fill: 'backwards' });
        }
      });
    }

    // Compteur
    if (list.length !== lastCount) {
      var from = lastCount, to = list.length, t0 = performance.now();
      (function f(now) {
        var p = Math.min(1, (now - t0) / 400);
        countEl.textContent = Math.round(from + (to - from) * p);
        if (p < 1) requestAnimationFrame(f);
      })(t0);
      lastCount = to;
    } else countEl.textContent = list.length;
    $('count-label').textContent = list.length > 1 ? 'véhicules correspondent' : (list.length ? 'véhicule correspond' : 'véhicule ne correspond');

    // Curseurs
    $('prix-out').textContent = s.prix >= maxPrix ? 'Sans limite' : PL.fmtPrice(s.prix);
    $('km-out').textContent = s.km >= maxKm ? 'Sans limite' : PL.fmtKm(s.km);
    [prix, km].forEach(function (r) {
      r.style.setProperty('--p', ((r.value - r.min) / (r.max - r.min) * 100) + '%');
    });

    // Filtres actifs
    var pills = [];
    if (s.q) pills.push(['q', '« ' + s.q + ' »']);
    if (s.marque) pills.push(['marque', s.marque]);
    s.carburant.forEach(function (c) { pills.push(['carburant:' + c, c]); });
    s.boite.forEach(function (c) { pills.push(['boite:' + c, c]); });
    if (s.prix < maxPrix) pills.push(['prix', 'Jusqu\'à ' + PL.fmtPrice(s.prix)]);
    if (s.km < maxKm) pills.push(['km', 'Moins de ' + PL.fmtKm(s.km)]);
    if (s.annee) pills.push(['annee', 'Depuis ' + s.annee]);
    $('active').innerHTML = pills.map(function (p) {
      return '<button type="button" data-clear="' + PL.esc(p[0]) + '" aria-label="Retirer le filtre ' + PL.esc(p[1]) + '">' + PL.esc(p[1]) +
        '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4l8 8M12 4l-8 8" stroke-linecap="round"/></svg></button>';
    }).join('');
    $('f-badge').textContent = pills.length ? '(' + pills.length + ')' : '';
  }

  function clear(key) {
    var parts = key.split(':');
    if (parts[0] === 'q') $('q').value = '';
    if (parts[0] === 'marque') $('marque').value = '';
    if (parts[0] === 'prix') prix.value = maxPrix;
    if (parts[0] === 'km') km.value = maxKm;
    if (parts[0] === 'annee') $('annee').value = '';
    if (parts[1]) $(parts[0]).querySelectorAll('input').forEach(function (i) { if (i.value === parts[1]) i.checked = false; });
  }
  function resetAll() {
    $('q').value = ''; $('marque').value = ''; $('annee').value = '';
    prix.value = maxPrix; km.value = maxKm;
    document.querySelectorAll('#carburant input, #boite input').forEach(function (i) { i.checked = false; });
    render(true);
  }

  /* ---------- Événements ---------- */
  var tId;
  $('q').addEventListener('input', function () { clearTimeout(tId); tId = setTimeout(function () { render(true); }, 180); });
  ['marque', 'annee', 'sort'].forEach(function (id) { $(id).addEventListener('change', function () { render(true); }); });
  ['carburant', 'boite'].forEach(function (id) { $(id).addEventListener('change', function () { render(true); }); });
  [prix, km].forEach(function (r) {
    r.addEventListener('input', function () { clearTimeout(tId); tId = setTimeout(function () { render(true); }, 60); });
  });
  $('reset').addEventListener('click', resetAll);
  grid.addEventListener('click', function (e) { if (e.target.closest('#empty-reset')) resetAll(); });
  $('active').addEventListener('click', function (e) {
    var b = e.target.closest('[data-clear]');
    if (b) { clear(b.getAttribute('data-clear')); render(true); }
  });

  // Tiroir de filtres (mobile)
  var panel = $('filters'), scrim = $('scrim'), toggle = $('f-toggle');
  function drawer(open) {
    panel.classList.toggle('is-open', open);
    scrim.classList.toggle('is-on', open);
    toggle.setAttribute('aria-expanded', open);
    if (open) panel.querySelector('input, select').focus({ preventScroll: true });
  }
  toggle.addEventListener('click', function () { drawer(true); });
  $('filters-close').addEventListener('click', function () { drawer(false); toggle.focus(); });
  scrim.addEventListener('click', function () { drawer(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && panel.classList.contains('is-open')) drawer(false); });

  /* ---------- Filtres reçus par l'URL (?carburant=Hybride&marque=Peugeot&q=…) ---------- */
  var params = PL.params();
  if (params.get('q')) $('q').value = params.get('q');
  if (params.get('marque')) $('marque').value = params.get('marque');
  ['carburant', 'boite'].forEach(function (k) {
    var val = params.get(k);
    if (val) $(k).querySelectorAll('input').forEach(function (i) { if (i.value === val) i.checked = true; });
  });

  render(false);
})();
