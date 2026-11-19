(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  var nfEur = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
  var nfNum = new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 0 });
  function eur(n) { return isFinite(n) ? nfEur.format(Math.round(n)) : '—'; }
  function pct(n, d) { return isFinite(n) ? n.toFixed(d === undefined ? 1 : d).replace('.', ',') + ' %' : '—'; }

  /* Valeur future d'un versement mensuel + capital initial */
  function fv(initial, monthly, annualRate, years) {
    var i = annualRate / 100 / 12, n = Math.round(years * 12);
    if (i === 0) return initial + monthly * n;
    return initial * Math.pow(1 + i, n) + monthly * (Math.pow(1 + i, n) - 1) / i;
  }
  /* Mensualité d'un crédit amortissable */
  function pmt(capital, annualRate, years) {
    var i = annualRate / 100 / 12, n = Math.round(years * 12);
    if (n === 0) return 0;
    if (i === 0) return capital / n;
    return capital * i / (1 - Math.pow(1 + i, -n));
  }
  function cssVar(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  /* ---------- Fabrique de contrôles ---------- */
  function slider(o) {
    var w = document.createElement('div'); w.className = 'ctl';
    w.innerHTML = '<div class="lab"><span>' + o.label + '</span><span class="val"></span></div>' +
      '<input type="range" min="' + o.min + '" max="' + o.max + '" step="' + o.step + '" value="' + o.value + '" id="' + o.id + '">';
    var inp = $('input', w), val = $('.val', w);
    function sync() { val.textContent = o.fmt(+inp.value); }
    inp.addEventListener('input', function () { sync(); o.on(); });
    sync();
    return { el: w, input: inp, get: function () { return +inp.value; } };
  }
  function select(o) {
    var w = document.createElement('div'); w.className = 'ctl';
    var opts = o.options.map(function (x, k) {
      return '<option value="' + x.v + '"' + (k === o.index ? ' selected' : '') + '>' + x.t + '</option>';
    }).join('');
    w.innerHTML = '<div class="lab"><span>' + o.label + '</span></div><select id="' + o.id + '">' + opts + '</select>';
    var inp = $('select', w);
    inp.addEventListener('change', o.on);
    return { el: w, input: inp, get: function () { return +inp.value; } };
  }
  function cells(defs) {
    var w = document.createElement('div'); w.className = 'out';
    w.innerHTML = defs.map(function (d) {
      return '<div class="cell"><div class="k">' + d.k + '</div><div class="v ' + (d.c || '') + '" data-o="' + d.id +
        '">—</div>' + (d.sub ? '<div class="s" data-s="' + d.id + '"></div>' : '') + '</div>';
    }).join('');
    return w;
  }
  function shell(host, kicker, title, lede) {
    host.className = 'sim';
    host.removeAttribute('data-widget');
    host.innerHTML = '<div class="sim-head"><div class="k">' + kicker + '</div><h4>' + title + '</h4><p>' + lede + '</p></div>' +
      '<div class="sim-body"></div>';
    return $('.sim-body', host);
  }

  /* ---------- 1. Épargne de précaution ---------- */
  function wPrecaution(host) {
    var b = shell(host, 'Simulateur', 'Votre épargne de précaution',
      'Calculez votre cible en mois de dépenses, et le temps nécessaire pour l’atteindre.');
    var out = cells([
      { k: 'Cible', id: 'cible', c: 'gold' },
      { k: 'Déjà constitué', id: 'deja' },
      { k: 'Reste à épargner', id: 'reste' },
      { k: 'Délai', id: 'delai', sub: 1 }
    ]);
    var s1 = slider({ id: 'pr-dep', label: 'Dépenses mensuelles', min: 500, max: 6000, step: 50, value: 2300, fmt: eur, on: run });
    var s2 = select({
      id: 'pr-prof', label: 'Votre situation', index: 1, on: run, options: [
        { v: 3, t: 'CDI stable, sans personne à charge — 3 mois' },
        { v: 4.5, t: 'CDI avec enfants, ou propriétaire — 4 à 6 mois' },
        { v: 6, t: 'CDD, intérim, période d’essai — 6 mois' },
        { v: 9, t: 'Indépendant, artisan, libéral — 6 à 12 mois' },
        { v: 12, t: 'Revenus très irréguliers — 12 mois' }
      ]
    });
    var s3 = slider({ id: 'pr-act', label: 'Épargne disponible aujourd’hui', min: 0, max: 40000, step: 250, value: 4000, fmt: eur, on: run });
    var s4 = slider({ id: 'pr-eff', label: 'Capacité d’épargne mensuelle', min: 25, max: 2000, step: 25, value: 250, fmt: eur, on: run });
    var g = document.createElement('div'); g.className = 'grid2';
    g.appendChild(s3.el); g.appendChild(s4.el);
    b.appendChild(s1.el); b.appendChild(s2.el); b.appendChild(g); b.appendChild(out);
    var note = document.createElement('div'); note.className = 'simnote'; b.appendChild(note);

    function run() {
      var cible = s1.get() * s2.get(), reste = Math.max(0, cible - s3.get());
      var mois = s4.get() > 0 ? Math.ceil(reste / s4.get()) : Infinity;
      $('[data-o=cible]', out).textContent = eur(cible);
      $('[data-o=deja]', out).textContent = eur(s3.get());
      $('[data-o=reste]', out).textContent = eur(reste);
      var d = $('[data-o=delai]', out);
      if (reste === 0) { d.textContent = 'Atteinte'; d.className = 'v gold'; }
      else if (!isFinite(mois)) { d.textContent = '—'; d.className = 'v'; }
      else { d.textContent = mois + (mois > 1 ? ' mois' : ' mois'); d.className = 'v'; }
      $('[data-s=delai]', out).textContent = reste === 0 ? 'Objectif couvert' :
        (isFinite(mois) ? 'soit ' + (mois / 12).toFixed(1).replace('.', ',') + ' an(s)' : '');
      note.innerHTML = reste === 0
        ? '<strong>Votre coussin est complet.</strong> Arrêtez de l’alimenter et redirigez vos ' + eur(s4.get()) +
          ' mensuels vers l’investissement — c’est l’étape 4 de la séquence du chapitre 16.'
        : '<strong>Priorité au coussin.</strong> Tant que la cible n’est pas atteinte, cette épargne passe avant tout investissement en actifs volatils. Elle vous donne le droit de ne jamais vendre au mauvais moment.';
    }
    run();
  }

  /* ---------- 2. Intérêts composés ---------- */
  function wCompound(host) {
    var b = shell(host, 'Simulateur', 'La force des intérêts composés',
      'Voyez la part de votre capital final qui vient de vos versements, et celle qui vient du rendement.');
    var s1 = slider({ id: 'ic-mens', label: 'Versement mensuel', min: 0, max: 2000, step: 25, value: 300, fmt: eur, on: run });
    var s2 = slider({ id: 'ic-init', label: 'Capital de départ', min: 0, max: 100000, step: 500, value: 0, fmt: eur, on: run });
    var s3 = slider({ id: 'ic-taux', label: 'Rendement annuel moyen', min: 0, max: 10, step: 0.25, value: 6, fmt: function (v) { return pct(v, 2); }, on: run });
    var s4 = slider({ id: 'ic-duree', label: 'Durée', min: 5, max: 40, step: 1, value: 30, fmt: function (v) { return v + ' ans'; }, on: run });
    var g1 = document.createElement('div'); g1.className = 'grid2'; g1.appendChild(s1.el); g1.appendChild(s2.el);
    var g2 = document.createElement('div'); g2.className = 'grid2'; g2.appendChild(s3.el); g2.appendChild(s4.el);
    var out = cells([
      { k: 'Capital final', id: 'fin', c: 'gold' },
      { k: 'Total versé', id: 'vers' },
      { k: 'Gains', id: 'gains' },
      { k: 'Part des gains', id: 'part', sub: 1 }
    ]);
    var cv = document.createElement('canvas');
    var lg = document.createElement('div'); lg.className = 'legend';
    lg.innerHTML = '<span><i style="background:var(--ink-3)"></i>Vos versements</span><span><i style="background:var(--gold)"></i>Gains générés</span>';
    var note = document.createElement('div'); note.className = 'simnote';
    b.appendChild(g1); b.appendChild(g2); b.appendChild(out); b.appendChild(cv); b.appendChild(lg); b.appendChild(note);

    var series = [];
    function run() {
      var m = s1.get(), init = s2.get(), r = s3.get(), y = s4.get();
      var total = fv(init, m, r, y), versed = init + m * y * 12, gains = total - versed;
      $('[data-o=fin]', out).textContent = eur(total);
      $('[data-o=vers]', out).textContent = eur(versed);
      $('[data-o=gains]', out).textContent = eur(gains);
      $('[data-o=part]', out).textContent = total > 0 ? pct(gains / total * 100, 0) : '—';
      $('[data-s=part]', out).textContent = 'du capital final';
      series = [];
      for (var k = 0; k <= y; k++) series.push({ t: fv(init, m, r, k), v: init + m * k * 12 });
      draw();
      var late = fv(init, m, r, Math.max(0, y - 10));
      note.innerHTML = '<strong>Le coût du report.</strong> En commençant 10 ans plus tard, avec les mêmes versements, vous obtiendriez ' +
        eur(late) + ' au lieu de ' + eur(total) + ' — soit <strong>' + eur(total - late) +
        ' de moins</strong> pour seulement ' + eur(m * 120) + ' de versements économisés.';
    }
    function draw() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = cv.clientWidth || 600, h = cv.clientHeight || 190;
      cv.width = w * dpr; cv.height = h * dpr;
      var c = cv.getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0);
      c.clearRect(0, 0, w, h);
      var surf = cssVar('--surface-2') || '#f5f1ea', line = cssVar('--line') || '#e6dfd2';
      var gold = cssVar('--gold') || '#a8762c', base = cssVar('--ink-3') || '#7a7263';
      c.fillStyle = surf; c.fillRect(0, 0, w, h);
      if (!series.length) return;
      var max = series[series.length - 1].t || 1, pad = 10;
      var X = function (k) { return pad + k / (series.length - 1 || 1) * (w - pad * 2); };
      var Y = function (v) { return h - pad - (v / max) * (h - pad * 2); };
      c.strokeStyle = line; c.lineWidth = 1;
      for (var q = 1; q <= 3; q++) {
        var yy = Math.round(h - pad - (q / 4) * (h - pad * 2)) + 0.5;
        c.beginPath(); c.moveTo(pad, yy); c.lineTo(w - pad, yy); c.stroke();
      }
      function area(key, fill) {
        c.beginPath(); c.moveTo(X(0), Y(0));
        series.forEach(function (p, k) { c.lineTo(X(k), Y(p[key])); });
        c.lineTo(X(series.length - 1), Y(0)); c.closePath();
        c.fillStyle = fill; c.fill();
      }
      area('t', gold); area('v', base);
    }
    window.addEventListener('resize', draw);
    if (window.matchMedia) {
      var mq = window.matchMedia('(prefers-color-scheme: dark)');
      (mq.addEventListener ? mq.addEventListener.bind(mq, 'change') : mq.addListener.bind(mq))(draw);
    }
    run();
    setTimeout(draw, 60);
  }

  /* ---------- 3. Impact des frais ---------- */
  function wFees(host) {
    var b = shell(host, 'Simulateur', 'Ce que vos frais coûtent vraiment',
      'Les frais se composent comme les rendements, mais en votre défaveur — et ils sont certains.');
    var s1 = slider({ id: 'fr-mens', label: 'Versement mensuel', min: 25, max: 2000, step: 25, value: 300, fmt: eur, on: run });
    var s2 = slider({ id: 'fr-duree', label: 'Durée', min: 5, max: 40, step: 1, value: 30, fmt: function (v) { return v + ' ans'; }, on: run });
    var s3 = slider({ id: 'fr-brut', label: 'Rendement brut annuel', min: 2, max: 10, step: 0.25, value: 6, fmt: function (v) { return pct(v, 2); }, on: run });
    var s4 = slider({ id: 'fr-a', label: 'Contrat à frais faibles', min: 0, max: 1.5, step: 0.05, value: 0.3, fmt: function (v) { return pct(v, 2); }, on: run });
    var s5 = slider({ id: 'fr-b', label: 'Contrat à frais élevés', min: 0.2, max: 3.5, step: 0.05, value: 1.5, fmt: function (v) { return pct(v, 2); }, on: run });
    var g1 = document.createElement('div'); g1.className = 'grid2'; g1.appendChild(s1.el); g1.appendChild(s2.el);
    var g2 = document.createElement('div'); g2.className = 'grid2'; g2.appendChild(s4.el); g2.appendChild(s5.el);
    var out = cells([
      { k: 'Frais faibles', id: 'a', c: 'gold' },
      { k: 'Frais élevés', id: 'bb' },
      { k: 'Écart', id: 'ec', c: 'warn', sub: 1 }
    ]);
    var note = document.createElement('div'); note.className = 'simnote';
    b.appendChild(s3.el); b.appendChild(g1); b.appendChild(g2); b.appendChild(out); b.appendChild(note);
    function run() {
      var m = s1.get(), y = s2.get(), brut = s3.get();
      var A = fv(0, m, Math.max(0, brut - s4.get()), y), B = fv(0, m, Math.max(0, brut - s5.get()), y);
      var versed = m * y * 12;
      $('[data-o=a]', out).textContent = eur(A);
      $('[data-o=bb]', out).textContent = eur(B);
      $('[data-o=ec]', out).textContent = eur(A - B);
      $('[data-s=ec]', out).textContent = versed > 0 ? pct((A - B) / versed * 100, 0) + ' de vos versements' : '';
      note.innerHTML = '<strong>Un écart certain, pas espéré.</strong> ' + pct(s5.get() - s4.get(), 2) +
        ' de frais annuels en plus coûtent ' + eur(A - B) + ' sur ' + y +
        ' ans. Vous payez ces frais les bonnes comme les mauvaises années : c’est le seul gain de performance totalement garanti de votre stratégie.';
    }
    run();
  }

  /* ---------- 4. Allocation et perte maximale ---------- */
  function wRisk(host) {
    var b = shell(host, 'Simulateur', 'Votre part actions, convertie en euros',
      'La bonne allocation n’est pas celle qui rapporte le plus : c’est celle que vous tiendrez pendant une crise.');
    var s1 = slider({ id: 'rk-cap', label: 'Capital investi', min: 1000, max: 500000, step: 1000, value: 60000, fmt: eur, on: run });
    var s2 = slider({ id: 'rk-act', label: 'Part en actions', min: 0, max: 100, step: 5, value: 60, fmt: function (v) { return v + ' %'; }, on: run });
    var out = cells([
      { k: 'Baisse envisageable', id: 'bai', c: 'warn' },
      { k: 'Valeur au plus bas', id: 'bas' },
      { k: 'Profil', id: 'pro', sub: 1 }
    ]);
    var note = document.createElement('div'); note.className = 'simnote';
    b.appendChild(s1.el); b.appendChild(s2.el); b.appendChild(out); b.appendChild(note);
    function run() {
      var cap = s1.get(), a = s2.get(), perte = cap * (a / 100) * 0.45;
      $('[data-o=bai]', out).textContent = '− ' + eur(perte);
      $('[data-o=bas]', out).textContent = eur(cap - perte);
      var p = a <= 30 ? 'Prudent' : a <= 65 ? 'Équilibré' : 'Dynamique';
      var hz = a <= 30 ? '3 à 6 ans' : a <= 65 ? '8 à 15 ans' : '15 ans et plus';
      $('[data-o=pro]', out).textContent = p;
      $('[data-s=pro]', out).textContent = 'horizon ' + hz;
      note.innerHTML = '<strong>Le test à passer.</strong> « Mes ' + eur(cap) + ' deviennent ' + eur(cap - perte) +
        ' pendant dix-huit mois, et je continue à verser chaque mois pendant cette période. » Si cette phrase vous paraît insupportable, votre part actions est trop élevée — baissez le curseur jusqu’à ce qu’elle devienne acceptable.';
    }
    run();
  }

  /* ---------- 5. Cash-flow locatif ---------- */
  function wCashflow(host) {
    var b = shell(host, 'Simulateur', 'Cash-flow d’un investissement locatif',
      'Le calcul complet : coût total, charges réelles, mensualité — et l’effort d’épargne qui en découle.');
    var s = {};
    function mk(id, label, min, max, step, value, fmt) {
      s[id] = slider({ id: 'cf-' + id, label: label, min: min, max: max, step: step, value: value, fmt: fmt, on: run });
      return s[id].el;
    }
    var pctf = function (v) { return pct(v, 1); };
    var g1 = document.createElement('div'); g1.className = 'grid2';
    g1.appendChild(mk('prix', 'Prix d’achat', 30000, 600000, 5000, 150000, eur));
    g1.appendChild(mk('trav', 'Travaux', 0, 120000, 500, 8500, eur));
    var g2 = document.createElement('div'); g2.className = 'grid2';
    g2.appendChild(mk('notaire', 'Frais de notaire', 2, 9, 0.1, 7.7, pctf));
    g2.appendChild(mk('loyer', 'Loyer mensuel hors charges', 200, 3000, 25, 750, eur));
    var g3 = document.createElement('div'); g3.className = 'grid2';
    g3.appendChild(mk('taux', 'Taux du crédit (hors assurance)', 1, 7, 0.1, 3.5, pctf));
    g3.appendChild(mk('duree', 'Durée du crédit', 10, 25, 1, 20, function (v) { return v + ' ans'; }));
    var g4 = document.createElement('div'); g4.className = 'grid2';
    g4.appendChild(mk('assur', 'Assurance emprunteur (par an)', 0, 1, 0.05, 0.3, pctf));
    g4.appendChild(mk('charges', 'Charges fixes annuelles (foncier, copro, PNO, comptable)', 0, 6000, 50, 2050, eur));
    var g5 = document.createElement('div'); g5.className = 'grid2';
    g5.appendChild(mk('gestion', 'Gestion + provision travaux', 0, 30, 1, 15, function (v) { return v + ' % des loyers'; }));
    var out = cells([
      { k: 'Coût total', id: 'cout' },
      { k: 'Mensualité', id: 'mens' },
      { k: 'Cash-flow mensuel', id: 'cf', sub: 1 },
      { k: 'Rendement brut', id: 'rb' },
      { k: 'Rendement net de charges', id: 'rn' }
    ]);
    var note = document.createElement('div'); note.className = 'simnote';
    b.appendChild(g1); b.appendChild(g2); b.appendChild(g3); b.appendChild(g4); b.appendChild(g5);
    b.appendChild(out); b.appendChild(note);

    function run() {
      var prix = s.prix.get(), trav = s.trav.get();
      var cout = prix * (1 + s.notaire.get() / 100) + trav;
      var loyerAn = s.loyer.get() * 12;
      var loyerReel = loyerAn * 0.96;                       /* provision de vacance : 4 % */
      var chAn = s.charges.get() + loyerAn * s.gestion.get() / 100;
      var net = loyerReel - chAn;
      var m = pmt(cout, s.taux.get(), s.duree.get()) + cout * s.assur.get() / 100 / 12;
      var cf = net / 12 - m;
      $('[data-o=cout]', out).textContent = eur(cout);
      $('[data-o=mens]', out).textContent = eur(m);
      var e = $('[data-o=cf]', out);
      e.textContent = (cf >= 0 ? '+ ' : '− ') + eur(Math.abs(cf));
      e.className = 'v ' + (cf >= 0 ? 'gold' : 'warn');
      $('[data-s=cf]', out).textContent = cf >= 0 ? 'le bien s’autofinance' : 'effort d’épargne mensuel';
      $('[data-o=rb]', out).textContent = pct(loyerAn / cout * 100, 2);
      $('[data-o=rn]', out).textContent = pct(net / cout * 100, 2);
      var effort = Math.abs(cf) * 12 * s.duree.get();
      note.innerHTML = cf >= 0
        ? '<strong>Cash-flow positif.</strong> Vérifiez que les provisions sont réalistes avant de conclure : vacance, impayés, gros travaux et hausse de la taxe foncière sont les quatre postes systématiquement sous-estimés. Et faites valider le régime fiscal par un expert-comptable avant de signer.'
        : '<strong>Effort d’épargne : ' + eur(Math.abs(cf)) + ' par mois</strong>, soit ' + eur(effort) + ' sur ' + s.duree.get() +
          ' ans. Ce n’est pas disqualifiant — c’est une épargne forcée qui construit un actif en partie financé par le locataire — mais ce projet ne « s’autofinance » pas. Sachez-le avant de signer, pas après.';
    }
    run();
  }

  var WIDGETS = { precaution: wPrecaution, compound: wCompound, fees: wFees, risk: wRisk, cashflow: wCashflow };
  $$('.widget[data-widget]').forEach(function (el) {
    var fn = WIDGETS[el.getAttribute('data-widget')];
    if (fn) { el.style.display = 'block'; try { fn(el); } catch (e) { console.error("widget", el.getAttribute("data-widget"), e); } }
  });

  /* ---------- Tableaux défilables ---------- */
  $$('.reader table').forEach(function (t) {
    if (t.parentNode && t.parentNode.classList.contains('tablewrap')) return;
    var w = document.createElement('div'); w.className = 'tablewrap';
    t.parentNode.insertBefore(w, t); w.appendChild(t);
  });

  /* ---------- Cases à cocher actives et mémorisées ---------- */
  var KEY = 'am-checks-v1', saved = {};
  try { saved = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { saved = {}; }
  $$('ul.task-list input[type=checkbox]').forEach(function (c, k) {
    c.disabled = false;
    c.id = c.id || 'chk-' + k;
    if (saved[c.id]) c.checked = true;
    c.addEventListener('change', function () {
      saved[c.id] = c.checked;
      try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch (e) { /* stockage indisponible */ }
    });
  });

  /* ---------- Navigation ---------- */
  var toc = $('#toc'), links = $$('#toc a'), bar = $('#progress > i'), now = $('#topbar .now');
  var targets = links.map(function (a) { return document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1))); });

  function closeNav() { document.body.classList.remove('nav-open'); }
  var btn = $('#navbtn');
  if (btn) btn.addEventListener('click', function () { document.body.classList.toggle('nav-open'); });
  var scrim = $('#scrim');
  if (scrim) scrim.addEventListener('click', closeNav);
  links.forEach(function (a) { a.addEventListener('click', closeNav); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeNav(); });

  var current = -1;
  function spy() {
    var y = window.scrollY + 110, idx = 0;
    for (var k = 0; k < targets.length; k++) {
      if (targets[k] && targets[k].offsetTop <= y) idx = k; else break;
    }
    if (idx !== current) {
      current = idx;
      links.forEach(function (a, k) { a.classList.toggle('on', k === idx); });
      if (now && links[idx]) now.textContent = links[idx].getAttribute('data-label') || links[idx].textContent;
      var a = links[idx];
      if (a && toc && window.innerWidth > 980) {
        var r = a.getBoundingClientRect(), rr = toc.getBoundingClientRect();
        if (r.top < rr.top + 40 || r.bottom > rr.bottom - 40) {
          toc.scrollTop += r.top - rr.top - toc.clientHeight / 2;
        }
      }
    }
    var h = document.documentElement.scrollHeight - window.innerHeight;
    if (bar) bar.style.width = (h > 0 ? Math.min(100, window.scrollY / h * 100) : 0) + '%';
  }
  var tick = false;
  window.addEventListener('scroll', function () {
    if (tick) return; tick = true;
    requestAnimationFrame(function () { spy(); tick = false; });
  }, { passive: true });
  window.addEventListener('resize', spy);
  spy();
})();
