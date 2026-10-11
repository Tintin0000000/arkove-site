/* Accueil */
(function () {
  var PL = window.PL;

  /* ---------- Titre : effet d'étirement + balayage "phares" ---------- */
  var title = document.getElementById('hero-title');
  if (title) {
    var st = PL.stretch(title, { base: 72, max: 125, gBase: 820, gMax: 900, radius: 300 });
    PL.ready(function () {
      setTimeout(function () { st.sweep().then(st.enable); }, PL.reduced ? 0 : 750);
    });
  }

  /* ---------- Parallaxe de la photo vedette ---------- */
  var heroPh = document.getElementById('hero-ph');
  if (heroPh && !PL.reduced) {
    var px = 0, py = 0, sy = 0, raf = null;
    function paint() {
      raf = null;
      heroPh.style.transform = 'translate3d(' + px + 'px,' + (py + sy) + 'px,0)';
    }
    window.addEventListener('scroll', function () {
      sy = Math.min(window.scrollY, 900) * 0.08;
      if (!raf) raf = requestAnimationFrame(paint);
    }, { passive: true });
    if (PL.fine) {
      heroPh.parentNode.addEventListener('pointermove', function (e) {
        var r = heroPh.parentNode.getBoundingClientRect();
        px = ((e.clientX - r.left) / r.width - .5) * -22;
        py = ((e.clientY - r.top) / r.height - .5) * -16;
        if (!raf) raf = requestAnimationFrame(paint);
      });
      heroPh.parentNode.addEventListener('pointerleave', function () { px = py = 0; if (!raf) raf = requestAnimationFrame(paint); });
    }
  }

  /* ---------- Vitrine : rail glissable ---------- */
  var rail = document.getElementById('rail');
  if (rail) {
    rail.innerHTML = PL.vehicles.filter(function (v) { return v.vitrine; }).map(PL.cardHTML).join('');
    PL.initPh(rail);
    PL.tilt(rail);

    var prev = document.querySelector('[data-rail="prev"]');
    var next = document.querySelector('[data-rail="next"]');
    var bar = document.querySelector('.rail-progress i');
    function step() {
      var c = rail.firstElementChild;
      return c ? c.getBoundingClientRect().width + 20 : 300;
    }
    function update() {
      var max = rail.scrollWidth - rail.clientWidth;
      var p = max > 0 ? rail.scrollLeft / max : 1;
      if (bar) bar.style.transform = 'scaleX(' + (0.15 + 0.85 * p) + ')';
      if (prev) prev.disabled = rail.scrollLeft < 4;
      if (next) next.disabled = rail.scrollLeft > max - 4;
    }
    rail.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
    if (prev) prev.addEventListener('click', function () { rail.scrollBy({ left: -step(), behavior: 'smooth' }); });
    if (next) next.addEventListener('click', function () { rail.scrollBy({ left: step(), behavior: 'smooth' }); });
    rail.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { rail.scrollBy({ left: step(), behavior: 'smooth' }); e.preventDefault(); }
      if (e.key === 'ArrowLeft') { rail.scrollBy({ left: -step(), behavior: 'smooth' }); e.preventDefault(); }
    });

    // Glisser à la souris, avec inertie
    var down = false, moved = false, sx = 0, sl = 0, vx = 0, lx = 0, lt = 0;
    rail.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse' || e.button !== 0) return;
      down = true; moved = false; sx = lx = e.clientX; sl = rail.scrollLeft; vx = 0; lt = performance.now();
    });
    window.addEventListener('pointermove', function (e) {
      if (!down) return;
      var dx = e.clientX - sx;
      if (!moved && Math.abs(dx) > 6) { moved = true; rail.classList.add('is-dragging'); }
      if (!moved) return;
      var now = performance.now();
      vx = (e.clientX - lx) / Math.max(1, now - lt); lx = e.clientX; lt = now;
      rail.scrollLeft = sl - dx;
    });
    window.addEventListener('pointerup', function () {
      if (!down) return;
      down = false;
      if (!moved) return;
      var v = vx * 16;
      (function glide() {
        if (Math.abs(v) < .5) { rail.classList.remove('is-dragging'); return; }
        rail.scrollLeft -= v; v *= .94;
        requestAnimationFrame(glide);
      })();
    });
    rail.addEventListener('click', function (e) { if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; } }, true);
  }

  /* ---------- Services : aperçu photo qui suit le curseur ---------- */
  var list = document.querySelector('.svc-list');
  var preview = document.querySelector('.svc-preview');
  if (list && preview && PL.fine && !PL.reduced) {
    var phs = preview.querySelectorAll('.ph');
    var tx = 0, ty = 0, cx = 0, cy = 0, rot = 0, on = false, looping = false;
    function loop() {
      var dx = tx - cx;
      cx += dx * .14; cy += (ty - cy) * .14;
      rot += ((dx * .04) - rot) * .1;
      rot = Math.max(-10, Math.min(10, rot));
      preview.style.transform = 'translate(' + cx + 'px,' + cy + 'px) translate(-50%,-50%) rotate(' + rot + 'deg) scale(' + (on ? 1 : .6) + ')';
      if (on || Math.abs(dx) > .5) requestAnimationFrame(loop); else looping = false;
    }
    list.addEventListener('pointerenter', function (e) {
      on = true; preview.classList.add('is-on');
      if (!cx) { cx = tx = e.clientX; cy = ty = e.clientY; }
      if (!looping) { looping = true; requestAnimationFrame(loop); }
    });
    list.addEventListener('pointerleave', function () { on = false; preview.classList.remove('is-on'); });
    list.addEventListener('pointermove', function (e) {
      tx = e.clientX; ty = e.clientY;
      var a = e.target.closest('[data-preview]');
      if (a) {
        var i = +a.getAttribute('data-preview');
        phs.forEach(function (p, k) { p.classList.toggle('is-active', k === i); });
      }
    });
  }

  /* ---------- Plaque : saisie formatée ---------- */
  var form = document.getElementById('plate-form');
  if (form) {
    var input = form.querySelector('#immat');
    var err = form.querySelector('#immat-err');
    PL.plateInput(input);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!/^[A-Z]{2}-\d{3}-[A-Z]{2}$/.test(input.value)) {
        err.textContent = input.value ? 'Format attendu : deux lettres, trois chiffres, deux lettres (AB-123-CD).' : 'Saisissez votre immatriculation pour continuer.';
        input.focus();
        input.closest('.plate').animate(
          [{ transform: 'translateX(0)' }, { transform: 'translateX(-8px)' }, { transform: 'translateX(8px)' }, { transform: 'translateX(-4px)' }, { transform: 'translateX(0)' }],
          { duration: 380, easing: 'ease-out' });
        return;
      }
      err.textContent = '';
      var url = 'contact.html?demande=reprise&immat=' + encodeURIComponent(input.value);
      if (PL.reduced) { location.href = url; return; }
      try { sessionStorage.setItem('pl-nav', '1'); } catch (x) {}
      document.documentElement.classList.add('is-leaving');
      setTimeout(function () { location.href = url; }, 640);
    });
  }
})();
