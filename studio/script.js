/* ══════════════════════════════════════════════════════════════
   ARKOVE STUDIO — moteur d'animation (vanilla, zéro dépendance)
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var FINE    = matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };
  var lerp  = function (a, b, t) { return a + (b - a) * t; };

  /* ───────── registre rAF unique ───────── */
  var jobs = [];
  function onFrame(fn) { jobs.push(fn); }
  (function tick(t) {
    for (var i = 0; i < jobs.length; i++) jobs[i](t);
    requestAnimationFrame(tick);
  })(0);

  /* ───────── 1. DÉCOUPE TYPOGRAPHIQUE ───────── */
  $$('[data-split]').forEach(function (el) {
    var txt = el.textContent, out = '', i = 0;
    for (var c = 0; c < txt.length; c++) {
      var ch = txt[c];
      if (ch === ' ') { out += ' '; continue; }
      out += '<span class="ch" style="animation-delay:' + (0.22 + i * 0.026).toFixed(3) + 's">' + ch + '</span>';
      i++;
    }
    el.innerHTML = out;
  });
  $$('.fx-fade').forEach(function (el) {
    el.style.animationDelay = (0.2 + (+el.dataset.d || 0) * 0.055).toFixed(3) + 's';
  });

  /* ───────── 2. PRÉLOADER ───────── */
  var loader = $('#loader');
  function start() { document.body.classList.add('ready'); }

  if (REDUCED || !loader) {
    if (loader) loader.style.display = 'none';
    start();
  } else {
    var num = $('#loNum'), arc = $('#loArc'), val = 0, target = 0, t0 = performance.now();
    var assets = Promise.race([
      new Promise(function (r) { window.addEventListener('load', r, { once: true }); }),
      new Promise(function (r) { setTimeout(r, 2600); })
    ]);
    var loaded = false;
    assets.then(function () { loaded = true; });

    var loopId = setInterval(function () {
      var elapsed = performance.now() - t0;
      target = loaded ? 100 : Math.min(92, elapsed / 14);
      val = lerp(val, target, 0.12);
      if (num) num.textContent = Math.round(val);
      if (arc) arc.style.strokeDashoffset = 327 - (327 * val) / 100;
      if (val > 99.4 && loaded) {
        clearInterval(loopId);
        if (num) num.textContent = '100';
        if (arc) arc.style.strokeDashoffset = '0';
        setTimeout(function () {
          loader.classList.add('done');
          start();
          setTimeout(function () { loader.style.display = 'none'; }, 1500);
        }, 260);
      }
    }, 16);
  }

  /* ───────── 3. THÈME ───────── */
  var root = document.documentElement, tgl = $('#themeToggle');
  try {
    var saved = localStorage.getItem('arkove-theme');
    if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved);
  } catch (e) {}
  if (tgl) tgl.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    var go = function () { root.setAttribute('data-theme', next); try { localStorage.setItem('arkove-theme', next); } catch (e) {} };
    if (document.startViewTransition && !REDUCED) document.startViewTransition(go); else go();
  });

  /* ───────── 4. CURSEUR SUR MESURE ───────── */
  if (FINE && !REDUCED) {
    var cur = $('#cursor'), label = $('.cur-label', cur);
    var cx = -200, cy = -200, tx = cx, ty = cy, rx = cx, ry = cy;
    var dot = $('.cur-dot', cur), ring = $('.cur-ring', cur);

    addEventListener('mousemove', function (e) {
      tx = e.clientX; ty = e.clientY; cur.classList.add('on');
    }, { passive: true });
    addEventListener('mouseleave', function () { cur.classList.remove('on'); });

    onFrame(function () {
      cx = lerp(cx, tx, 0.9); cy = lerp(cy, ty, 0.9);
      rx = lerp(rx, tx, 0.17); ry = lerp(ry, ty, 0.17);
      dot.style.transform  = 'translate(' + cx + 'px,' + cy + 'px) translate(-50%,-50%)';
      ring.style.transform = 'translate(' + rx + 'px,' + ry + 'px) translate(-50%,-50%)';
      label.style.transform = 'translate(' + rx + 'px,' + ry + 'px) translate(-50%,-50%)';
    });

    var HOVER = 'a,button,input,textarea,[data-tilt],[data-cursor],.q,.lab-card';
    document.addEventListener('mouseover', function (e) {
      var t = e.target.closest(HOVER);
      if (!t) return;
      cur.classList.add('grow');
      var l = t.closest('[data-cursor]');
      label.textContent = l ? l.dataset.cursor : '';
    });
    document.addEventListener('mouseout', function (e) {
      if (e.target.closest(HOVER)) { cur.classList.remove('grow'); label.textContent = ''; }
    });
  }

  /* ───────── 5. BARRE DE PROGRESSION + NAV ───────── */
  var nav = $('#nav'), bar = $('#progressBar'), lastY = 0;
  function onScrollUI() {
    var y = scrollY;
    var h = document.documentElement.scrollHeight - innerHeight;
    if (bar) bar.style.width = (h > 0 ? clamp(y / h, 0, 1) * 100 : 0) + '%';
    if (nav) {
      nav.classList.toggle('stuck', y > 40);
      nav.classList.toggle('hide', y > 460 && y > lastY && !document.body.classList.contains('lock'));
    }
    lastY = y;
  }
  addEventListener('scroll', onScrollUI, { passive: true });
  onScrollUI();

  /* ───────── 5 bis. BARRE D'APPEL MOBILE ───────── */
  var callbar = $('#callbar'), contactSec = $('#contact');
  if (callbar) {
    var contactVisible = false;
    if (contactSec) {
      new IntersectionObserver(function (e) { contactVisible = e[0].isIntersecting; }, { threshold: 0.12 })
        .observe(contactSec);
    }
    addEventListener('scroll', function () {
      callbar.classList.toggle('show', scrollY > innerHeight * 0.75 && !contactVisible);
    }, { passive: true });
  }

  /* ───────── 6. MENU MOBILE ───────── */
  var burger = $('#burger'), menu = $('#menu');
  if (burger && menu) {
    var toggleMenu = function (force) {
      var open = force !== undefined ? force : !menu.classList.contains('open');
      menu.classList.toggle('open', open);
      burger.classList.toggle('on', open);
      burger.setAttribute('aria-expanded', open);
      menu.setAttribute('aria-hidden', !open);
      document.body.classList.toggle('lock', open);
    };
    burger.addEventListener('click', function () { toggleMenu(); });
    $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { toggleMenu(false); }); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') toggleMenu(false); });
  }

  /* ───────── 7. RÉVÉLATIONS AU SCROLL ───────── */
  var revealables = $$('.rv, .tl-step');
  if (REDUCED) {
    revealables.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('in');
        io.unobserve(e.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    // décalage en cascade au sein d'une même grille
    [['.mani-grid', 3], ['.works-grid', 3], ['.lab-grid', 3], ['.bat-grid', 4]].forEach(function (pair) {
      $$(pair[0]).forEach(function (grid) {
        $$('.rv', grid).forEach(function (el, i) { el.style.transitionDelay = (i % pair[1]) * 0.08 + 's'; });
      });
    });
    revealables.forEach(function (el) { io.observe(el); });
  }

  /* ───────── 8. COMPTEURS ───────── */
  function runCounter(el) {
    var to = parseFloat(el.dataset.to) || 0, sfx = el.dataset.suffix || '';
    if (REDUCED) { el.textContent = to + sfx; return; }
    var dur = 1500, t0 = null;
    (function step(ts) {
      if (t0 === null) t0 = ts;
      var p = clamp((ts - t0) / dur, 0, 1);
      var e = 1 - Math.pow(1 - p, 4);
      el.textContent = Math.round(to * e).toLocaleString('fr-FR') + sfx;
      if (p < 1) requestAnimationFrame(step);
    })(performance.now());
  }
  var cio = new IntersectionObserver(function (ents) {
    ents.forEach(function (e) { if (e.isIntersecting) { runCounter(e.target); cio.unobserve(e.target); } });
  }, { threshold: 0.6 });
  $$('.cnt').forEach(function (el) { cio.observe(el); });

  /* ───────── 9. MANIFESTE : mots éclairés au scroll ───────── */
  var mani = $('[data-words]');
  if (mani) {
    var words = mani.textContent.trim().split(/\s+/);
    mani.innerHTML = words.map(function (w) { return '<span class="w">' + w + '</span>'; }).join(' ');
    var spans = $$('.w', mani);
    if (REDUCED) spans.forEach(function (s) { s.classList.add('lit'); });
    else onFrame(function () {
      var r = mani.getBoundingClientRect();
      if (r.bottom < 0 || r.top > innerHeight) return;
      var p = clamp((innerHeight * 0.82 - r.top) / (r.height + innerHeight * 0.28), 0, 1);
      var n = Math.round(p * spans.length);
      if (n === mani._lit) return;              // rien n'a changé : pas de recalcul de style
      var from = mani._lit || 0;
      if (n > from) for (var i = from; i < n; i++) spans[i].classList.add('lit');
      else for (var j = from - 1; j >= n; j--) spans[j].classList.remove('lit');
      mani._lit = n;
    });
  }

  /* ───────── 10. SCROLL HORIZONTAL ÉPINGLÉ ───────── */
  var hz = $('#hz'), hzTrack = $('#hzTrack'), hzBar = $('#hzBar');
  if (hz && hzTrack && !REDUCED && innerWidth > 760) {
    var hzX = 0, hzTargetX = 0;
    onFrame(function () {
      var r = hz.getBoundingClientRect();
      if (r.bottom < -200 || r.top > innerHeight + 200) return;
      var dist = hzTrack.scrollWidth - innerWidth + 40;
      var total = hz.offsetHeight - innerHeight;
      var p = clamp(-r.top / (total || 1), 0, 1);
      hzTargetX = -p * Math.max(dist, 0);
      hzX = lerp(hzX, hzTargetX, 0.1);
      hzTrack.style.transform = 'translate3d(' + hzX.toFixed(2) + 'px,0,0)';
      if (hzBar) hzBar.style.width = (p * 100).toFixed(1) + '%';
    });
  }

  /* ───────── 11. TIMELINE : trait qui se dessine ───────── */
  var tl = $('#timeline'), tlFg = $('#tlFg');
  if (tl && tlFg) onFrame(function () {
    var r = tl.getBoundingClientRect();
    if (r.bottom < 0 || r.top > innerHeight) return;
    var p = clamp((innerHeight * 0.72 - r.top) / (r.height * 0.86), 0, 1);
    tlFg.style.strokeDashoffset = (1000 - 1000 * p).toFixed(1);
  });

  /* ───────── 12. MARQUEES (vitesse liée au scroll) ───────── */
  function marquee(track, baseSpeed) {
    if (!track || REDUCED) return;
    var html = track.innerHTML;
    track.innerHTML = html + html;              // boucle sans couture
    var x = 0, w = 0, vel = 0, prevY = scrollY;
    var measure = function () { w = track.scrollWidth / 2; };
    measure();
    addEventListener('resize', measure);
    addEventListener('scroll', function () {
      vel = clamp((scrollY - prevY) * 0.42, -26, 26);
      prevY = scrollY;
    }, { passive: true });
    onFrame(function () {
      vel = lerp(vel, 0, 0.06);
      x -= baseSpeed + vel * Math.sign(baseSpeed || 1);
      if (w && x <= -w) x += w;
      if (w && x > 0) x -= w;
      track.style.transform = 'translate3d(' + x.toFixed(2) + 'px,0,0)';
    });
  }
  marquee($('.ticker-track'), 0.6);
  marquee($('.q-track'), 0.35);

  /* ───────── 13. INCLINAISON 3D + SPOT LUMINEUX ───────── */
  if (FINE && !REDUCED) {
    $$('[data-tilt], .mani-card').forEach(function (el) {
      var rx = 0, ry = 0, trx = 0, try_ = 0, active = false;
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
        trx = (0.5 - py) * 8; try_ = (px - 0.5) * 8;
        el.style.setProperty('--mx', (px * 100).toFixed(1) + '%');
        el.style.setProperty('--my', (py * 100).toFixed(1) + '%');
        active = true;
      });
      el.addEventListener('mouseleave', function () { trx = 0; try_ = 0; active = false; });
      onFrame(function () {
        if (!active && Math.abs(rx) < 0.01 && Math.abs(ry) < 0.01) return;
        rx = lerp(rx, trx, 0.12); ry = lerp(ry, try_, 0.12);
        el.style.transform = 'perspective(900px) rotateX(' + rx.toFixed(2) + 'deg) rotateY(' + ry.toFixed(2) + 'deg)' +
                             (active ? ' translateY(-5px)' : '');
      });
    });
  }

  /* ───────── 14. BOUTONS MAGNÉTIQUES ───────── */
  if (FINE && !REDUCED) {
    $$('.magnet').forEach(function (el) {
      var x = 0, y = 0, tx = 0, ty = 0;
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        tx = (e.clientX - (r.left + r.width / 2)) * 0.3;
        ty = (e.clientY - (r.top + r.height / 2)) * 0.45;
      });
      el.addEventListener('mouseleave', function () { tx = 0; ty = 0; });
      onFrame(function () {
        if (Math.abs(x - tx) < 0.05 && Math.abs(y - ty) < 0.05) return;
        x = lerp(x, tx, 0.16); y = lerp(y, ty, 0.16);
        el.style.transform = 'translate(' + x.toFixed(2) + 'px,' + y.toFixed(2) + 'px)';
      });
    });
  }

  /* ───────── 15. TEXTE BROUILLÉ ───────── */
  var GLYPHS = '#@%$&*!?/\\<>[]{}ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  function scramble(el, text, speed) {
    if (REDUCED) { el.textContent = text; return; }
    var frame = 0, queue = [], old = el.dataset.scTxt || el.textContent;
    el.dataset.scTxt = text;
    var len = Math.max(old.length, text.length);
    for (var i = 0; i < len; i++) {
      queue.push({ from: old[i] || '', to: text[i] || '', start: Math.floor(Math.random() * 14), end: Math.floor(Math.random() * 18) + 14 });
    }
    if (el._sc) cancelAnimationFrame(el._sc);
    (function run() {
      var out = '', done = 0;
      for (var i = 0; i < queue.length; i++) {
        var q = queue[i];
        if (frame >= q.end) { done++; out += q.to; }
        else if (frame >= q.start) {
          if (!q.ch || Math.random() < 0.3) q.ch = GLYPHS[Math.floor(Math.random() * GLYPHS.length)];
          out += '<span class="sc-x">' + q.ch + '</span>';
        } else out += q.from;
      }
      el.innerHTML = out;
      if (done < queue.length) { frame += speed || 1; el._sc = requestAnimationFrame(run); }
    })();
  }
  if (FINE) $$('[data-scramble]').forEach(function (el) {
    var txt = el.textContent;
    el.addEventListener('mouseenter', function () { scramble(el, txt, 1.4); });
  });

  var scBox = $('#scrambleBox');
  if (scBox) {
    var list = scBox.dataset.words.split(','), k = 0;
    var cycle = function () { k = (k + 1) % list.length; scramble(scBox, list[k], 1); };
    var sio = new IntersectionObserver(function (e) {
      if (e[0].isIntersecting && !scBox._timer && !REDUCED) scBox._timer = setInterval(cycle, 2200);
      else if (!e[0].isIntersecting && scBox._timer) { clearInterval(scBox._timer); scBox._timer = null; }
    }, { threshold: 0.4 });
    sio.observe(scBox);
    scBox.addEventListener('mouseenter', cycle);
  }

  /* ───────── 16. LAB ───────── */
  var liquid = $('#liquidBtn');
  if (liquid) liquid.addEventListener('click', function (e) {
    var r = liquid.getBoundingClientRect(), s = document.createElement('i');
    s.className = 'ripple';
    s.style.left = (e.clientX - r.left) + 'px';
    s.style.top = (e.clientY - r.top) + 'px';
    s.style.width = s.style.height = '14px';
    liquid.appendChild(s);
    setTimeout(function () { s.remove(); }, 700);
  });

  var gooey = $('#gooey');
  if (gooey) {
    var gBtn = $('.goo-main', gooey);
    gBtn.addEventListener('click', function () {
      var open = gooey.classList.toggle('on');
      gBtn.setAttribute('aria-expanded', open);
    });
  }

  var dialRange = $('#dialRange'), dialVal = $('#dialVal'), dialNum = $('#dialNum');
  if (dialRange && dialVal) {
    var setDial = function () {
      var v = +dialRange.value, lo = +dialRange.min || 0, hi = +dialRange.max || 100;
      var p = (v - lo) / (hi - lo || 1);
      dialVal.style.strokeDashoffset = 289 - 289 * p;
      var unit = dialRange.dataset.unit || '';
      dialNum.textContent = v;
      if (unit) dialNum.insertAdjacentHTML('beforeend', '<i>' + unit + '</i>');
    };
    dialRange.addEventListener('input', setDial);
    setDial();
  }

  var stack = $('#stack'), stackBtn = $('#stackBtn');
  if (stack && stackBtn) {
    var order = [0, 1, 2];
    var paint = function () {
      $$('i', stack).forEach(function (card, i) {
        var pos = order.indexOf(i);
        card.style.transform = 'translate(' + pos * 10 + 'px,' + pos * -7 + 'px) scale(' + (1 - pos * 0.06) + ')';
        card.style.zIndex = 3 - pos;
      });
    };
    stackBtn.addEventListener('click', function () { order.push(order.shift()); paint(); });
    paint();
  }

  /* ───────── 16 bis. QUESTIONS FRÉQUENTES ───────── */
  $$('.faq-i').forEach(function (item, i) {
    var btn = $('.faq-q', item), panel = $('.faq-a', item);
    if (!btn || !panel) return;
    panel.id = 'faq-a-' + i;
    btn.setAttribute('aria-controls', panel.id);
    btn.addEventListener('click', function () {
      var open = !item.classList.contains('open');
      // une seule réponse ouverte à la fois
      $$('.faq-i.open').forEach(function (o) {
        if (o === item) return;
        o.classList.remove('open');
        var b = $('.faq-q', o); if (b) b.setAttribute('aria-expanded', 'false');
      });
      item.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open);
    });
  });

  /* ───────── 17. FORMULAIRE ───────── */
  var form = $('form[name="studio"]');
  if (form) form.addEventListener('submit', function (e) {
    if (!form.checkValidity()) { form.reportValidity(); e.preventDefault(); return; }
    var local = location.protocol === 'file:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1';
    e.preventDefault();
    var finish = function () {
      var btn = $('.submit', form), note = $('#formNote');
      if (btn) btn.classList.add('ok');
      if (note) note.classList.add('show');
      form.reset();
      setTimeout(function () { if (btn) btn.classList.remove('ok'); }, 4200);
    };
    if (local) { finish(); return; }
    fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                 body: new URLSearchParams(new FormData(form)).toString() })
      .then(finish).catch(function () { form.submit(); });
  });

  /* ───────── 18. HORLOGE / ANNÉE / HAUT DE PAGE ───────── */
  var clock = $('#clock');
  if (clock) (function tickClock() {
    clock.textContent = new Date().toLocaleTimeString('fr-FR', { hour12: false });
    setTimeout(tickClock, 1000);
  })();
  var yr = $('#year'); if (yr) yr.textContent = new Date().getFullYear();
  var toTop = $('#toTop');
  if (toTop) toTop.addEventListener('click', function () {
    scrollTo({ top: 0, behavior: REDUCED ? 'auto' : 'smooth' });
  });

  /* ───────── 19. CANEVAS DU HÉRO — champ de particules ───────── */
  var cv = $('#heroCanvas');
  if (cv && !REDUCED) {
    var ctx = cv.getContext('2d', { alpha: true });
    var W = 0, H = 0, DPR = Math.min(devicePixelRatio || 1, 1.5);
    var parts = [], visible = true, mouse = { x: -9999, y: -9999 };

    // On lit le JETON --bg, pas background-color : les variables CSS ne
    // transitionnent pas, donc la valeur est exacte dès le changement de thème.
    function bgRGB() {
      var v = getComputedStyle(root).getPropertyValue('--bg').trim();
      var h = v.replace('#', '');
      if (/^[0-9a-f]{6}$/i.test(h)) {
        return parseInt(h.slice(0, 2), 16) + ',' + parseInt(h.slice(2, 4), 16) + ',' + parseInt(h.slice(4, 6), 16);
      }
      var c = v.match(/\d+/g);
      return c ? c.slice(0, 3).join(',') : '11,10,9';
    }
    function isLight() { return root.getAttribute('data-theme') === 'light'; }
    var trail = bgRGB(), light = isLight();
    function syncTheme() { trail = bgRGB(); light = isLight(); }
    new MutationObserver(syncTheme)
      .observe(root, { attributes: true, attributeFilter: ['data-theme'] });

    function resize() {
      var r = cv.getBoundingClientRect();
      W = r.width; H = r.height;
      cv.width = W * DPR; cv.height = H * DPR;
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      var n = Math.round(clamp((W * H) / 14000, 50, 140));
      parts = [];
      for (var i = 0; i < n; i++) {
        parts.push({
          x: Math.random() * W, y: Math.random() * H,
          vx: 0, vy: 0,
          s: Math.random() * 1.3 + 0.35,
          hue: Math.random() < 0.78 ? 'gold' : 'violet',
          o: Math.random() * 0.42 + 0.2
        });
      }
      ctx.clearRect(0, 0, W, H);
    }
    resize();
    addEventListener('resize', function () { clearTimeout(cv._rt); cv._rt = setTimeout(resize, 160); });

    cv.parentElement.addEventListener('mousemove', function (e) {
      var r = cv.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
    }, { passive: true });
    cv.parentElement.addEventListener('mouseleave', function () { mouse.x = mouse.y = -9999; });

    new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }, { threshold: 0.01 }).observe(cv);

    var time = 0;
    onFrame(function () {
      if (!visible || !W) return;
      time += 0.0022;
      ctx.fillStyle = 'rgba(' + trail + ',0.16)';
      ctx.fillRect(0, 0, W, H);

      for (var i = 0; i < parts.length; i++) {
        var p = parts[i];
        // champ de flux pseudo-bruité
        var a = Math.sin(p.x * 0.0036 + time * 2.1) * Math.cos(p.y * 0.0031 - time * 1.7) * Math.PI * 1.6;
        p.vx = lerp(p.vx, Math.cos(a) * 0.68, 0.06);
        p.vy = lerp(p.vy, Math.sin(a) * 0.68 - 0.1, 0.06);

        // répulsion au pointeur
        var dx = p.x - mouse.x, dy = p.y - mouse.y, d2 = dx * dx + dy * dy;
        if (d2 < 24000) {
          var f = (24000 - d2) / 24000 * 1.5, d = Math.sqrt(d2) || 1;
          p.vx += (dx / d) * f; p.vy += (dy / d) * f;
        }

        var ox = p.x, oy = p.y, wrapped = false;
        p.x += p.vx; p.y += p.vy;
        if (p.x < -20) { p.x = W + 20; wrapped = true; }
        else if (p.x > W + 20) { p.x = -20; wrapped = true; }
        if (p.y < -20) { p.y = H + 20; wrapped = true; }
        else if (p.y > H + 20) { p.y = -20; wrapped = true; }
        if (wrapped) continue;   // jamais de trait d'un bord à l'autre

        ctx.strokeStyle = light
          ? (p.hue === 'gold' ? 'rgba(146,98,24,' + (p.o * 0.75) + ')'
                              : 'rgba(69,52,196,' + (p.o * 0.6) + ')')
          : (p.hue === 'gold' ? 'rgba(217,163,85,' + p.o + ')'
                              : 'rgba(122,104,245,' + (p.o * 0.85) + ')');
        ctx.lineWidth = p.s;
        ctx.lineCap = 'round';
        ctx.beginPath(); ctx.moveTo(ox, oy); ctx.lineTo(p.x, p.y); ctx.stroke();
      }
    });
  }
})();
