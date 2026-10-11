/* ==========================================================================
   Comportements partagés par toutes les pages
   ========================================================================== */
(function () {
  window.PL = window.PL || {};
  var doc = document.documentElement;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(pointer: fine)').matches;
  PL.reduced = reduced;
  PL.fine = finePointer;

  /* ---------- File d'attente "page prête" (après ouverture du rideau) ---------- */
  var readyQueue = [], isReady = false;
  PL.ready = function (fn) { isReady ? fn() : readyQueue.push(fn); };
  function fireReady() {
    if (isReady) return;
    isReady = true;
    readyQueue.forEach(function (fn) { fn(); });
    readyQueue = [];
  }

  /* ---------- Emplacements photo ---------- */
  var ICONS = {
    car:
      '<svg class="car-line" viewBox="0 0 400 150" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
        '<path pathLength="1" d="M30 112h26a39 39 0 0 1 78 0h134a39 39 0 0 1 78 0h22c7 0 10-5 9-12l-3-14c-2-8-9-12-20-14l-58-7c-17-14-42-31-72-33l-76-1c-21 0-41 9-58 24l-30 17c-17 4-28 11-31 22l-2 11c0 4 2 7 7 7z"/>' +
        '<path class="d2" pathLength="1" d="M117 63l35-24c6-3 12-4 18-4h56c25 2 44 15 59 29z"/>' +
        '<line class="d2" pathLength="1" x1="196" y1="35" x2="196" y2="64"/>' +
        '<path class="d2" pathLength="1" d="M196 70l2 38M118 72h194"/>' +
        '<path class="d3" pathLength="1" d="M352 82l18 3M40 88h10"/>' +
        '<circle class="d3" pathLength="1" cx="95" cy="112" r="28"/><circle class="d3" pathLength="1" cx="307" cy="112" r="28"/>' +
        '<circle class="d3" pathLength="1" cx="95" cy="112" r="9"/><circle class="d3" pathLength="1" cx="307" cy="112" r="9"/>' +
        '<path class="d3" pathLength="1" d="M8 141h384"/>' +
      '</svg>',
    photo:
      '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 15h8l3-5h14l3 5h8v23H6z" stroke-linejoin="round"/><circle cx="24" cy="26" r="7"/></svg>',
    person:
      '<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="24" cy="17" r="8"/><path d="M8 42c2-9 8-14 16-14s14 5 16 14" stroke-linecap="round"/></svg>'
  };

  PL.initPh = function (root) {
    (root || document).querySelectorAll('.ph:not([data-ready])').forEach(function (el) {
      el.setAttribute('data-ready', '');
      var type = el.getAttribute('data-ph') || 'photo';
      var label = el.getAttribute('data-label');
      var hint = el.getAttribute('data-hint');
      var html = '<div class="ph-art">' + (ICONS[type] || ICONS.photo) + '</div>';
      if (label || hint) {
        html += '<div class="ph-cap"><b>' + (label || 'Photo à insérer') + '</b>' + (hint ? '<span>' + hint + '</span>' : '') + '</div>';
      }
      el.insertAdjacentHTML('afterbegin', html);
      el.setAttribute('role', 'img');
      el.setAttribute('aria-label', 'Emplacement photo : ' + (label || 'à compléter'));

      // Si le fichier existe, il remplace automatiquement l'emplacement.
      var src = el.getAttribute('data-src');
      if (src) {
        var img = new Image();
        img.alt = el.getAttribute('data-alt') || label || '';
        img.decoding = 'async';
        img.onload = function () { el.appendChild(img); requestAnimationFrame(function () { el.classList.add('has-photo'); }); };
        img.src = src;
      }
      if (type === 'car') drawObserver.observe(el);
    });
  };

  var drawObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('is-drawn'); drawObserver.unobserve(e.target); }
    });
  }, { threshold: 0.3 });

  /* ---------- Plaque : effet "split-flap" ---------- */
  var FLAP = 'ABCDEFGHJKLMNPRSTVWXYZ0123456789';
  PL.flap = function (el, opts) {
    opts = opts || {};
    var final = el.getAttribute('data-flap') || el.textContent;
    el.innerHTML = final.split('').map(function (c) {
      return '<span class="' + (c === '-' ? 'dash' : '') + '">' + c + '</span>';
    }).join('');
    if (reduced) return Promise.resolve();
    var spans = el.querySelectorAll('span');
    var start = performance.now();
    var base = opts.base || 380, step = opts.step || 95;
    return new Promise(function (resolve) {
      var last = 0;
      (function tick(now) {
        var t = now - start, done = true;
        if (now - last > 55) {
          last = now;
          spans.forEach(function (s, i) {
            if (final[i] === '-') return;
            if (t < base + i * step) { s.textContent = FLAP[(Math.random() * FLAP.length) | 0]; done = false; }
            else s.textContent = final[i];
          });
        } else done = false;
        done ? resolve() : requestAnimationFrame(tick);
      })(start);
    });
  };

  /* ---------- Rideau métallique : entrée ---------- */
  var shutter = document.getElementById('shutter');
  function raiseShutter() {
    if (!shutter || !doc.classList.contains('is-entering')) { fireReady(); return; }
    shutter.classList.add('is-up');
    setTimeout(fireReady, 380);
    setTimeout(function () {
      doc.classList.remove('is-entering', 'is-intro');
      shutter.classList.remove('is-up');
    }, 1050);
  }

  function enter() {
    var fromNav = false;
    try { fromNav = !!sessionStorage.getItem('pl-nav'); sessionStorage.removeItem('pl-nav'); } catch (e) {}
    if (!doc.classList.contains('is-entering')) { fireReady(); return; }
    var fontsReady = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();
    var plateNum = shutter && shutter.querySelector('[data-flap]');
    if (!fromNav && plateNum) {
      // Première visite de l'accueil : intro complète
      doc.classList.add('is-intro');
      try { sessionStorage.setItem('pl-intro', '1'); } catch (e) {}
      fontsReady.then(function () {
        return PL.flap(plateNum);
      }).then(function () { setTimeout(raiseShutter, 520); });
    } else {
      Promise.race([fontsReady, new Promise(function (r) { setTimeout(r, 600); })])
        .then(function () { setTimeout(raiseShutter, 120); });
    }
  }

  /* ---------- Paramètres de page ----------
     Certains hébergeurs (aperçus, iframes) retirent la query string :
     on la mémorise au clic et on la relit en secours. */
  function pageKey(path) { return 'pl-q:' + (path.split('/').pop() || 'index.html'); }
  PL.rememberQuery = function (url) {
    try {
      if (url.search) sessionStorage.setItem(pageKey(url.pathname), url.search);
      else sessionStorage.removeItem(pageKey(url.pathname));
    } catch (e) {}
  };
  PL.params = function () {
    var s = location.search;
    if (!s || s.length < 2) { try { s = sessionStorage.getItem(pageKey(location.pathname)) || ''; } catch (e) {} }
    return new URLSearchParams(s);
  };

  /* ---------- Rideau métallique : sortie ---------- */
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest('a[href]');
    if (!a || a.target || a.hasAttribute('download')) return;
    var url = new URL(a.href, location.href);
    if (url.origin !== location.origin || !/^https?:|^file:/.test(url.protocol)) return;
    PL.rememberQuery(url);
    if (url.pathname === location.pathname && url.search === location.search) return; // ancre interne
    if (!shutter || reduced) return;
    e.preventDefault();
    try { sessionStorage.setItem('pl-nav', '1'); } catch (err) {}
    document.body.classList.remove('menu-open');
    doc.classList.add('is-leaving');
    setTimeout(function () { location.href = url.href; }, 640);
  });
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) { doc.classList.remove('is-leaving', 'is-entering', 'is-intro'); fireReady(); }
  });

  /* ---------- Navigation ---------- */
  var nav = document.querySelector('.nav');
  var road = document.querySelector('.road i');
  var lastY = 0, ticking = false;
  function onScroll() {
    var y = window.scrollY;
    if (nav) {
      nav.classList.toggle('is-solid', y > 12);
      nav.classList.toggle('is-hidden', y > 500 && y > lastY + 2 && !document.body.classList.contains('menu-open'));
      if (y < lastY - 2) nav.classList.remove('is-hidden');
    }
    if (road) {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      road.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, y / max) : 0) + ')';
    }
    lastY = y;
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  var burger = document.querySelector('.nav-burger');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', open);
      burger.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('menu-open')) burger.click();
    });
  }

  /* ---------- Révélations ---------- */
  // Les éléments .wipe sont masqués par clip-path (surface visible nulle) :
  // on observe donc leur parent, et on révèle l'élément associé.
  var revealIO = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      (e.target._reveal || [e.target]).forEach(function (el, i) { setTimeout(function () { el.classList.add('in'); }, i * 90); });
      revealIO.unobserve(e.target);
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -6% 0px' });
  PL.observeReveals = function (root) {
    (root || document).querySelectorAll('.lines:not([data-hero]), .wipe:not([data-hero])').forEach(function (el) {
      if (reduced) { el.classList.add('in'); return; }
      var target = el.classList.contains('wipe') ? el.parentElement : el;
      if (target !== el) (target._reveal = target._reveal || []).push(el);
      revealIO.observe(target);
    });
  };
  PL.ready(function () {
    document.querySelectorAll('[data-hero]').forEach(function (el, i) {
      setTimeout(function () { el.classList.add('in'); }, reduced ? 0 : i * 90);
    });
  });

  /* ---------- Texte étirable (axe de largeur variable) ---------- */
  PL.splitChars = function (el) {
    var walker = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (child) {
        if (child.nodeType === 3) {
          var frag = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach(function (word) {
            if (!word) return;
            if (/^\s+$/.test(word)) { frag.appendChild(document.createTextNode(' ')); return; }
            var w = document.createElement('span');
            w.style.display = 'inline-block';
            w.style.whiteSpace = 'nowrap';
            word.split('').forEach(function (c) {
              var s = document.createElement('span');
              s.className = 'ch';
              s.textContent = c;
              w.appendChild(s);
            });
            frag.appendChild(w);
          });
          child.parentNode.replaceChild(frag, child);
        } else if (child.nodeType === 1) walker(child);
      });
    };
    walker(el);
    return el.querySelectorAll('.ch');
  };

  PL.stretch = function (el, o) {
    o = o || {};
    var base = o.base || 72, max = o.max || 125, gBase = o.gBase || 820, gMax = o.gMax || 900, R = o.radius || 280;
    el.classList.add('stretch');
    var chars = PL.splitChars(el);
    var centers = [];
    function measure() {
      el.classList.add('is-live');
      chars.forEach(function (c) { c.style.setProperty('--w', base); c.style.setProperty('--g', gBase); });
      centers = Array.prototype.map.call(chars, function (c) {
        var r = c.getBoundingClientRect();
        return { x: r.left + r.width / 2 + window.scrollX, y: r.top + r.height / 2 + window.scrollY };
      });
      el.classList.remove('is-live');
    }
    function apply(px, py, live) {
      el.classList.toggle('is-live', !!live);
      for (var i = 0; i < chars.length; i++) {
        var dx = centers[i].x - px, dy = (centers[i].y - py) * 1.6;
        var d = Math.sqrt(dx * dx + dy * dy);
        var k = Math.max(0, 1 - d / R); k = k * k * (3 - 2 * k);
        chars[i].style.setProperty('--w', (base + (max - base) * k).toFixed(1));
        chars[i].style.setProperty('--g', (gBase + (gMax - gBase) * k).toFixed(0));
      }
    }
    function rest() {
      el.classList.remove('is-live');
      chars.forEach(function (c) { c.style.setProperty('--w', base); c.style.setProperty('--g', gBase); });
    }
    measure();
    window.addEventListener('resize', measure);
    if (document.fonts) document.fonts.ready.then(measure);

    // Balayage "phares" à l'arrivée
    function sweep() {
      if (reduced) return Promise.resolve();
      measure();
      var r = el.getBoundingClientRect();
      var y0 = r.top + window.scrollY + r.height / 2, x0 = r.left - R, x1 = r.right + R;
      var t0 = performance.now(), dur = o.sweepDur || 1700;
      return new Promise(function (resolve) {
        (function f(now) {
          var p = Math.min(1, (now - t0) / dur);
          var e = p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
          apply(x0 + (x1 - x0) * e, y0, true);
          if (p < 1) requestAnimationFrame(f); else { rest(); resolve(); }
        })(t0);
      });
    }

    var interactive = false;
    if (finePointer && !reduced && o.pointer !== false) {
      var raf = null, mx = 0, my = 0;
      window.addEventListener('pointermove', function (e) {
        if (!interactive) return;
        mx = e.pageX; my = e.pageY;
        if (!raf) raf = requestAnimationFrame(function () {
          raf = null;
          var r = el.getBoundingClientRect();
          var inside = e.clientY > r.top - R && e.clientY < r.bottom + R;
          inside ? apply(mx, my, true) : rest();
        });
      }, { passive: true });
      document.addEventListener('pointerleave', rest);
    }
    return {
      sweep: sweep,
      enable: function () { interactive = true; },
      measure: measure
    };
  };

  /* ---------- Curseur à étiquette ---------- */
  if (finePointer && !reduced) {
    doc.classList.add('has-cursor');
    var cur = document.createElement('div');
    cur.className = 'cursor';
    cur.setAttribute('aria-hidden', 'true');
    cur.innerHTML = '<div class="cursor-pill"></div>';
    document.body.appendChild(cur);
    var pill = cur.firstChild;
    var cx = -100, cy = -100, tx = -100, ty = -100, running = false;
    function loop() {
      cx += (tx - cx) * 0.22; cy += (ty - cy) * 0.22;
      cur.style.transform = 'translate3d(' + cx + 'px,' + cy + 'px,0)';
      if (Math.abs(tx - cx) > .1 || Math.abs(ty - cy) > .1) requestAnimationFrame(loop); else running = false;
    }
    window.addEventListener('pointermove', function (e) {
      tx = e.clientX; ty = e.clientY;
      if (!running) { running = true; requestAnimationFrame(loop); }
      var t = e.target.closest && e.target.closest('[data-cursor]');
      if (t) { pill.textContent = t.getAttribute('data-cursor'); cur.classList.add('is-label'); }
      else cur.classList.remove('is-label');
    }, { passive: true });
  }

  /* ---------- Boutons magnétiques ---------- */
  PL.magnetic = function (root) {
    if (!finePointer || reduced) return;
    (root || document).querySelectorAll('.magnetic').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        var x = e.clientX - r.left - r.width / 2, y = e.clientY - r.top - r.height / 2;
        el.style.transform = 'translate(' + x * .25 + 'px,' + y * .35 + 'px)';
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
  };

  /* ---------- Cartes : inclinaison + reflet ---------- */
  PL.tilt = function (root) {
    if (!finePointer || reduced) return;
    (root || document).querySelectorAll('.car:not([data-tilt])').forEach(function (card) {
      card.setAttribute('data-tilt', '');
      card.insertAdjacentHTML('beforeend', '<span class="spot" aria-hidden="true"></span>');
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
        card.style.setProperty('--mx', px * 100 + '%');
        card.style.setProperty('--my', py * 100 + '%');
        card.style.transform = 'perspective(900px) rotateY(' + (px - .5) * 5 + 'deg) rotateX(' + (.5 - py) * 5 + 'deg) translateY(-4px)';
      });
      card.addEventListener('pointerleave', function () {
        card.style.transition = 'transform .7s cubic-bezier(.16,1,.3,1), box-shadow .5s';
        card.style.transform = '';
        setTimeout(function () { card.style.transition = ''; }, 700);
      });
    });
  };

  /* ---------- Compteurs ---------- */
  PL.countUp = function (el, to, dur) {
    if (reduced) { el.textContent = to; return; }
    var t0 = performance.now(); dur = dur || 1200;
    (function f(now) {
      var p = Math.min(1, (now - t0) / dur);
      el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(f);
    })(t0);
  };

  /* ---------- Horaires (à confirmer avec Pierre-Lou) ---------- */
  // Index 0 = dimanche. Plages en heures décimales.
  PL.HOURS = [
    [],
    [[9, 12], [14, 19]],
    [[9, 12], [14, 19]],
    [[9, 12], [14, 19]],
    [[9, 12], [14, 19]],
    [[9, 12], [14, 19]],
    [[9, 12], [14, 18]]
  ];
  var DAYS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
  function hFmt(h) { var m = Math.round((h % 1) * 60); return Math.floor(h) + ' h' + (m ? (m < 10 ? '0' : '') + m : ''); }
  PL.hFmt = hFmt;
  PL.openStatus = function (now) {
    now = now || new Date();
    var d = now.getDay(), h = now.getHours() + now.getMinutes() / 60;
    var today = PL.HOURS[d];
    for (var i = 0; i < today.length; i++) {
      if (h >= today[i][0] && h < today[i][1]) return { open: true, text: 'Ouvert, ferme à ' + hFmt(today[i][1]) };
      if (h < today[i][0]) return { open: false, text: 'Fermé, ouvre à ' + hFmt(today[i][0]) };
    }
    for (var k = 1; k <= 7; k++) {
      var nd = (d + k) % 7;
      if (PL.HOURS[nd].length) {
        return { open: false, text: 'Fermé, ouvre ' + (k === 1 ? 'demain' : DAYS[nd]) + ' à ' + hFmt(PL.HOURS[nd][0][0]) };
      }
    }
    return { open: false, text: 'Fermé' };
  };
  document.querySelectorAll('[data-open]').forEach(function (el) {
    var s = PL.openStatus();
    el.textContent = s.text;
    el.classList.add('open-status', s.open ? 'is-open' : 'is-closed');
  });

  /* ---------- Plaque : saisie formatée AB-123-CD ---------- */
  PL.plateInput = function (input) {
    input.addEventListener('input', function () {
      var raw = input.value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 7);
      var out = raw.slice(0, 2);
      if (raw.length > 2) out += '-' + raw.slice(2, 5);
      if (raw.length > 5) out += '-' + raw.slice(5, 7);
      input.value = out;
    });
  };
  /* ---------- Divers ---------- */
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
  document.querySelectorAll('[data-stock]').forEach(function (el) { el.textContent = PL.vehicles ? PL.vehicles.length : ''; });

  // Footer : le grand nom réagit aussi au survol
  var giant = document.querySelector('.footer-giant');
  if (giant) {
    var g = PL.stretch(giant, { base: 62, max: 125, gBase: 900, gMax: 900, radius: 340 });
    g.enable();
  }

  PL.initPh();
  PL.observeReveals();
  PL.magnetic();
  PL.tilt();

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', enter);
  else enter();
})();
