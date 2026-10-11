/* Contact : formulaire adaptatif + horaires */
(function () {
  var PL = window.PL;
  var form = document.getElementById('contact-form');
  if (!form) return;
  var params = new URLSearchParams(location.search);

  /* ---------- Horaires ---------- */
  var DAYS = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'];
  var today = (new Date().getDay() + 6) % 7;
  document.querySelector('#hours tbody').innerHTML = DAYS.map(function (d, i) {
    var h = PL.HOURS[(i + 1) % 7];
    var txt = h.length ? h.map(function (r) { return PL.hFmt(r[0]) + '–' + PL.hFmt(r[1]); }).join(', ') : 'Fermé';
    return '<tr' + (i === today ? ' class="is-today"' : '') + '><td>' + d + '</td><td>' + txt + '</td></tr>';
  }).join('');

  /* ---------- Véhicules ---------- */
  var sel = document.getElementById('vehicule');
  sel.insertAdjacentHTML('beforeend', PL.vehicles.map(function (v) {
    return '<option value="' + v.id + '">' + PL.esc(v.marque + ' ' + v.modele + ', ' + v.annee + ', ' + PL.fmtPrice(v.prix)) + '</option>';
  }).join(''));
  var picked = document.getElementById('picked');
  function showPicked() {
    var v = PL.byId(sel.value);
    if (!v) { picked.innerHTML = ''; return; }
    picked.innerHTML = '<div class="picked-car"><div class="thumb"><div class="ph" data-ph="car" data-src="' + PL.photo(v, 1) + '"></div></div>' +
      '<div><b>' + PL.esc(v.marque + ' ' + v.modele) + '</b><span>' + PL.esc(v.version) + '<br>' + PL.fmtKm(v.km) + ', ' + PL.fmtPrice(v.prix) + '</span></div></div>';
    PL.initPh(picked);
    picked.firstChild.animate([{ opacity: 0, transform: 'translateY(8px)' }, { opacity: 1, transform: 'none' }], { duration: 400, easing: 'ease-out' });
  }
  sel.addEventListener('change', showPicked);

  /* ---------- Blocs selon la demande ---------- */
  var boxes = form.querySelectorAll('.reveal-box');
  function currentDemande() { return form.querySelector('input[name="demande"]:checked').value; }
  function syncBoxes() {
    var d = currentDemande();
    boxes.forEach(function (b) {
      var open = b.getAttribute('data-for').split(' ').indexOf(d) >= 0;
      b.classList.toggle('is-open', open);
      b.querySelectorAll('input, select, textarea').forEach(function (f) { f.tabIndex = open ? 0 : -1; });
      b.setAttribute('aria-hidden', !open);
    });
  }
  form.querySelectorAll('input[name="demande"]').forEach(function (r) { r.addEventListener('change', syncBoxes); });

  /* ---------- Plaque ---------- */
  var immat = document.getElementById('immat');
  PL.plateInput(immat);

  /* ---------- Pré-remplissage depuis l'URL ---------- */
  var d = params.get('demande');
  if (d) {
    var r = form.querySelector('input[name="demande"][value="' + d.replace(/[^a-z]/g, '') + '"]');
    if (r) r.checked = true;
  }
  if (params.get('vehicule') && PL.byId(params.get('vehicule'))) { sel.value = params.get('vehicule'); showPicked(); }
  if (params.get('essai')) document.getElementById('essai').checked = true;
  if (params.get('immat')) { immat.value = params.get('immat'); immat.dispatchEvent(new Event('input')); }
  if (params.get('vehicule') && d === 'reprise') {
    var v = PL.byId(params.get('vehicule'));
    if (v) document.getElementById('message').value = 'Reprise de ma voiture en vue de l\'achat de la ' + v.marque + ' ' + v.modele + ' (' + v.ref + ').';
  }
  syncBoxes();

  /* ---------- Validation ---------- */
  function setErr(input, msg) {
    var fld = input.closest('.fld');
    if (!fld) return;
    fld.classList.toggle('is-invalid', !!msg);
    fld.querySelector('.msg').textContent = msg || '';
    input.setAttribute('aria-invalid', !!msg);
  }
  var rules = {
    nom: function (v) { return v.trim().length < 2 ? 'Indiquez votre nom pour que Pierre-Loup sache qui rappeler.' : ''; },
    tel: function (v) { return v.replace(/\D/g, '').length < 10 ? 'Indiquez un numéro à 10 chiffres, par exemple 06 12 34 56 78.' : ''; },
    email: function (v) { return v && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? 'Cette adresse e-mail semble incomplète.' : ''; }
  };
  Object.keys(rules).forEach(function (k) {
    var input = document.getElementById(k);
    input.addEventListener('blur', function () { if (input.value) setErr(input, rules[k](input.value)); });
    input.addEventListener('input', function () { if (input.closest('.fld').classList.contains('is-invalid')) setErr(input, rules[k](input.value)); });
  });

  var done = document.getElementById('form-done');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var firstBad = null;
    Object.keys(rules).forEach(function (k) {
      var input = document.getElementById(k), msg = rules[k](input.value);
      setErr(input, msg);
      if (msg && !firstBad) firstBad = input;
    });
    var rgpd = document.getElementById('rgpd');
    if (!firstBad && !rgpd.checked) {
      firstBad = rgpd;
      rgpd.closest('.consent').animate([{ transform: 'translateX(0)' }, { transform: 'translateX(-6px)' }, { transform: 'translateX(6px)' }, { transform: 'translateX(0)' }], { duration: 320 });
    }
    if (firstBad) { firstBad.focus(); return; }

    // Maquette : aucun envoi réel. Brancher ici un service (Formspree, Brevo, e-mail…)
    var texts = {
      achat: 'Pierre-Loup vous rappelle dans la journée pour organiser la visite.',
      reprise: 'Pierre-Loup vous rappelle sous 24 h avec une estimation de reprise.',
      depot: 'Pierre-Loup vous rappelle pour convenir du dépôt de votre voiture.',
      financement: 'Pierre-Loup vous rappelle avec une proposition de financement.',
      recherche: 'Pierre-Loup lance la recherche et vous tient au courant.',
      autre: 'Pierre-Loup vous répond dans la journée.'
    };
    document.getElementById('done-text').textContent = texts[currentDemande()];
    done.classList.add('is-on');
    done.querySelector('button').focus({ preventScroll: true });
  });
  document.getElementById('again').addEventListener('click', function () {
    form.reset(); syncBoxes(); picked.innerHTML = '';
    done.classList.remove('is-on');
  });
})();
