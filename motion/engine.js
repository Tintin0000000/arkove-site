/*
 * Mini moteur de motion design.
 *
 * Une scène = une fonction pure du temps : render(t) reçoit le temps en secondes
 * et place chaque élément. Aucune animation CSS, aucun setTimeout : la même
 * valeur de t donne toujours la même image. C'est ce qui permet d'exporter
 * la vidéo image par image (voir render.mjs) sans saccade ni décalage.
 *
 * Dans le navigateur : barre de lecture, scrub, espace = play/pause.
 * Avec ?render=1 : pas d'interface, la scène attend que render.mjs appelle
 * window.__motion.seek(t) pour chaque image.
 */
(function () {
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, p) => a + (b - a) * p;

  const ease = {
    linear: (p) => p,
    outCubic: (p) => 1 - Math.pow(1 - p, 3),
    inCubic: (p) => p * p * p,
    inOutCubic: (p) => (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2),
    outExpo: (p) => (p === 1 ? 1 : 1 - Math.pow(2, -10 * p)),
    inOutExpo: (p) =>
      p === 0 ? 0 : p === 1 ? 1 : p < 0.5 ? Math.pow(2, 20 * p - 10) / 2 : (2 - Math.pow(2, -20 * p + 10)) / 2,
    outBack: (p) => {
      const c1 = 1.70158, c3 = c1 + 1;
      return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2);
    },
    outElastic: (p) => {
      if (p === 0 || p === 1) return p;
      return Math.pow(2, -10 * p) * Math.sin((p * 10 - 0.75) * ((2 * Math.PI) / 3)) + 1;
    },
  };

  // Progression 0 → 1 entre start et start + dur, avec easing.
  const prog = (t, start, dur, fn = ease.outCubic) => fn(clamp((t - start) / dur));

  // Format monétaire français : 7612 → "7 612 €"
  const euro = (v, decimals = 0) =>
    v.toLocaleString('fr-FR', { minimumFractionDigits: decimals, maximumFractionDigits: decimals }).replace(/ /g, ' ') + ' €';

  // Bruit pseudo-aléatoire déterministe (même graine = mêmes valeurs).
  const rng = (seed) => () => {
    seed = (seed * 1664525 + 1013904223) % 4294967296;
    return seed / 4294967296;
  };

  // Découpe le texte d'un élément en mots (span.w > span.wi) pour les animer.
  // Les espaces insécables (&nbsp;) ne coupent pas : « 1&nbsp;000&nbsp;€ » reste un bloc.
  const splitWords = (el) => {
    const words = el.textContent.trim().split(/[ \t\n\r]+/);
    el.innerHTML = words.map((w) => `<span class="w"><span class="wi">${w}</span></span>`).join(' ');
    return [...el.querySelectorAll('.wi')];
  };

  function scene({ width = 1080, height = 1920, duration, fps = 30, setup, render }) {
    const stage = document.getElementById('stage');
    stage.style.width = width + 'px';
    stage.style.height = height + 'px';
    const params = new URLSearchParams(location.search);
    const renderMode = params.has('render');
    document.documentElement.classList.toggle('render-mode', renderMode);

    let ctx = {};
    let t = 0;
    let ready = false;
    const seek = (time) => {
      t = clamp(time, 0, duration);
      if (ready) render(t, ctx);
    };

    // On attend les polices avant setup() : les mesures de texte en dépendent.
    const fonts = ['400 10px "Inter Tight"', '800 10px "Inter Tight"', '400 10px "Instrument Serif"',
      'italic 400 10px "Instrument Serif"', '700 10px "JetBrains Mono"'];
    const whenReady = Promise.all(fonts.map((f) => document.fonts.load(f))).catch(() => {}).then(() => {
      ctx = (setup && setup(stage)) || {};
      ready = true;
      seek(t);
    });

    window.__motion = { width, height, duration, fps, seek, ready: whenReady };

    if (renderMode) {
      stage.parentElement.style.width = width + 'px';
      stage.parentElement.style.height = height + 'px';
      return;
    }

    // --- Mode aperçu : mise à l'échelle + barre de lecture ---
    const fit = () => {
      const s = Math.min((innerWidth - 32) / width, (innerHeight - 96) / height);
      stage.style.transform = `scale(${s})`;
      stage.parentElement.style.width = width * s + 'px';
      stage.parentElement.style.height = height * s + 'px';
    };
    addEventListener('resize', fit);
    fit();

    const bar = document.createElement('div');
    bar.className = 'controls';
    bar.innerHTML = `
      <button type="button" class="play" aria-label="Lecture / pause">❚❚</button>
      <input type="range" min="0" max="${duration}" step="0.001" value="0" aria-label="Position">
      <span class="time">0.00 s</span>`;
    document.body.appendChild(bar);
    const btn = bar.querySelector('.play');
    const range = bar.querySelector('input');
    const label = bar.querySelector('.time');

    let playing = !params.has('pause');
    let last = performance.now();
    const sync = () => {
      range.value = t;
      label.textContent = `${t.toFixed(2)} / ${duration.toFixed(1)} s`;
      btn.textContent = playing ? '❚❚' : '▶';
    };
    const toggle = () => {
      if (!playing && t >= duration) seek(0);
      playing = !playing;
      last = performance.now();
      sync();
    };
    btn.addEventListener('click', toggle);
    addEventListener('keydown', (e) => {
      if (e.code === 'Space') { e.preventDefault(); toggle(); }
    });
    range.addEventListener('input', () => {
      playing = false;
      seek(parseFloat(range.value));
      sync();
    });

    const loop = (now) => {
      if (playing) {
        let next = t + (now - last) / 1000;
        if (next > duration + 0.6) next = 0; // courte pause puis boucle
        if (next <= duration) seek(next); else t = next;
        sync();
      }
      last = now;
      requestAnimationFrame(loop);
    };
    seek(0);
    sync();
    requestAnimationFrame(loop);
  }

  window.M = { clamp, lerp, ease, prog, euro, rng, splitWords, scene };
})();
