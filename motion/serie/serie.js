/*
 * Moteur de la série « Épargne malin ».
 *
 * Un épisode = un fichier epNN.json (voix + visuels + texte de publication).
 * build.py en tire epNN.html, qui charge ce fichier avec window.EP (l'épisode)
 * et window.VO (le minutage de la voix, produit par voix/voiceover.py).
 *
 * Chaque partie de la vidéo (« segment ») est un bloc visuel : hook, icon, counter,
 * bars, donut, grid, list, curves, timer, steps, cta. Les instants s'écrivent
 * "phrase:morceau" ("2:1" = début du 2e morceau de la 3e phrase), "2:end" pour la fin
 * de la phrase, avec un décalage optionnel : "2:1+0.4".
 */
(function () {
  const { prog, ease, clamp, lerp } = M;
  const EP = window.EP, VO = window.VO, S = VO.sentences;
  const $ = (sel, root = document) => root.querySelector(sel);
  const W = 1080;

  // ---------------------------------------------------------------- utilitaires

  const at = (ref) => {
    if (typeof ref === 'number') return ref;
    const m = String(ref).match(/^(\d+):(\w+)([+-][\d.]+)?$/);
    if (!m) throw new Error('Instant illisible : ' + ref);
    const s = S[+m[1]];
    const base = m[2] === 'end' ? s.end : m[2] === 'start' ? s.start : s.chunks[+m[2]].start;
    return base + (m[3] ? parseFloat(m[3]) : 0);
  };
  const fmt = (v, kind = 'euro') => {
    const n = Math.round(v).toLocaleString('fr-FR').replace(/[  ]/g, ' ');
    return kind === 'euro' ? n + ' €' : kind === 'pct' ? n + ' %' : kind === 'h' ? n + ' h' : n;
  };
  const html = (strings) => { const d = document.createElement('div'); d.innerHTML = strings.trim(); return d.firstElementChild; };
  const popIn = (el, p, rot = 0) => {
    el.style.opacity = clamp(p * 3);
    el.style.transform = `scale(${p}) rotate(${rot * (1 - p)}deg)`;
  };
  const rise = (el, p, dy = 60) => {
    el.style.opacity = clamp(p * 1.5);
    el.style.transform = `translateY(${(1 - p) * dy}px)`;
  };
  const COLORS = { gold: 'var(--gold-soft)', up: 'var(--up)', down: 'var(--down)', ink: 'var(--ink)', soft: 'var(--ink-soft)' };
  const col = (c) => COLORS[c] || c || COLORS.gold;

  // Icônes au trait (viewBox 100×100, couleur = currentColor).
  const ICONS = {
    wallet: '<rect x="10" y="26" width="80" height="58" rx="10"/><path d="M10 40 H90"/><path d="M66 56 H90 V70 H66 a7 7 0 0 1 0-14Z"/><path d="M20 26 L64 12 L72 26"/>',
    phone: '<rect x="28" y="8" width="44" height="84" rx="9"/><path d="M44 80 H56"/><path d="M38 30 L50 38 L38 46Z" fill="currentColor"/>',
    coffee: '<path d="M20 38 H72 V62 a22 22 0 0 1-22 22 H42 a22 22 0 0 1-22-22Z"/><path d="M72 46 h6 a10 10 0 0 1 0 20 h-8"/><path d="M36 14 q6 8 0 16 M52 14 q6 8 0 16"/><path d="M14 92 H80"/>',
    calendar: '<rect x="12" y="20" width="76" height="68" rx="10"/><path d="M12 40 H88 M32 10 V28 M68 10 V28"/><path d="M30 56 H40 M46 56 H56 M62 56 H72 M30 72 H40 M46 72 H56"/>',
    cart: '<path d="M8 16 H22 L32 64 H80 L90 30 H26"/><circle cx="38" cy="80" r="7"/><circle cx="74" cy="80" r="7"/>',
    chartDown: '<path d="M10 14 V88 H92"/><path d="M20 28 L40 46 L54 38 L84 72"/><path d="M84 52 V72 H64"/>',
    clock: '<circle cx="50" cy="52" r="38"/><path d="M50 30 V52 L66 62"/><path d="M38 8 H62"/>',
    envelope: '<rect x="8" y="22" width="84" height="58" rx="8"/><path d="M8 26 L50 56 L92 26"/>',
    cut: '<circle cx="28" cy="74" r="12"/><circle cx="72" cy="74" r="12"/><path d="M36 64 L78 12 M64 64 L22 12"/>',
    piggy: '<path d="M18 52 a32 26 0 0 1 32-26 h8 a32 26 0 0 1 28 18 h6 v14 h-8 a32 26 0 0 1-14 14 v12 h-12 v-8 h-16 v8 h-12 v-12 a32 26 0 0 1-12-20Z"/><path d="M44 26 a10 10 0 0 1 16 0"/><circle cx="72" cy="46" r="2.5" fill="currentColor"/><path d="M18 52 h-8"/>',
    shield: '<path d="M50 8 L86 20 V48 Q86 76 50 92 Q14 76 14 48 V20Z"/><path d="M34 50 L46 62 L68 38"/>',
    play: '<rect x="8" y="18" width="84" height="56" rx="10"/><path d="M42 34 L62 46 L42 58Z" fill="currentColor"/><path d="M30 86 H70"/>',
    dumbbell: '<path d="M26 50 H74"/><rect x="12" y="34" width="14" height="32" rx="4"/><rect x="74" y="34" width="14" height="32" rx="4"/><path d="M6 42 V58 M94 42 V58"/>',
    gamepad: '<path d="M22 32 H78 a14 14 0 0 1 14 16 l-4 22 a10 10 0 0 1-18 4 l-6-8 H34 l-6 8 a10 10 0 0 1-18-4 l-4-22 A14 14 0 0 1 22 32Z"/><path d="M30 44 V56 M24 50 H36"/><circle cx="66" cy="46" r="3" fill="currentColor"/><circle cx="74" cy="54" r="3" fill="currentColor"/>',
    basket: '<path d="M10 40 H90 L80 86 H20Z"/><path d="M30 40 L44 14 M70 40 L56 14"/><path d="M36 54 V72 M50 54 V72 M64 54 V72"/>',
    party: '<path d="M30 10 H70 L56 46 V78 M44 78 H68 M56 46 L44 10"/><path d="M36 92 H76"/><circle cx="20" cy="30" r="3" fill="currentColor"/><circle cx="84" cy="24" r="3" fill="currentColor"/>',
    bus: '<rect x="16" y="10" width="68" height="70" rx="12"/><path d="M16 46 H84 M16 28 H84"/><circle cx="32" cy="64" r="5"/><circle cx="68" cy="64" r="5"/><path d="M28 80 V90 M72 80 V90"/>',
    bolt: '<path d="M56 6 L22 56 H48 L42 94 L78 40 H52Z"/>',
    house: '<path d="M10 48 L50 14 L90 48"/><path d="M20 40 V88 H80 V40"/><path d="M42 88 V64 H58 V88"/>',
    bank: '<path d="M10 36 L50 12 L90 36Z"/><path d="M16 84 H84 M10 92 H90 M24 44 V76 M42 44 V76 M58 44 V76 M76 44 V76"/>',
    check: '<circle cx="50" cy="50" r="40"/><path d="M30 52 L44 66 L72 36"/>',
    cross: '<circle cx="50" cy="50" r="40"/><path d="M34 34 L66 66 M66 34 L34 66"/>',
    coin: '<circle cx="50" cy="50" r="40"/><path d="M62 32 a20 20 0 1 0 0 36 M30 46 H58 M30 56 H58"/>',
    moon: '<path d="M64 10 a40 40 0 1 0 26 66 a32 32 0 1 1-26-66Z"/><path d="M20 20 l4 8 l8 4 l-8 4 l-4 8 l-4-8 l-8-4 l8-4Z"/>',
  };
  const icon = (name, cls = '') => `<svg class="ic ${cls}" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">${ICONS[name] || ''}</svg>`;

  // ---------------------------------------------------------------- blocs

  const BLOCKS = {};

  // Gros mots qui claquent, une icône, puis la « réponse » en italique doré.
  BLOCKS.hook = {
    build(el, b) {
      el.insertAdjacentHTML('beforeend', `
        <div class="abs hk-icon" style="color:${col(b.iconColor || 'gold')}">${icon(b.icon)}</div>
        <div class="abs hk-lines">${b.lines.map((l) => `
          <div class="hw ${l.size || ''}" style="color:${l.color ? col(l.color) : 'var(--ink)'}">${l.hl ? '<i class="hl"></i>' : ''}<span>${l.text}</span></div>`).join('')}
        </div>
        ${b.reveal ? `<div class="abs hk-reveal">${b.reveal.html}</div>` : ''}`);
      return { icon: $('.hk-icon', el), lines: [...el.querySelectorAll('.hw')], box: $('.hk-lines', el), reveal: $('.hk-reveal', el) };
    },
    render(t, b, st) {
      const first = at(b.lines[0].at) - 0.15;
      const ip = prog(t, first, 0.6, ease.outBack);
      st.icon.style.opacity = clamp(ip * 3);
      st.icon.style.transform = `scale(${ip}) rotate(${(1 - ip) * -25 + Math.sin(t * 3) * 3}deg)`;
      b.lines.forEach((l, i) => {
        const p = prog(t, at(l.at), 0.4, ease.outBack);
        const el = st.lines[i];
        el.style.opacity = clamp(p * 3);
        el.style.transform = `scale(${lerp(1.7, 1, p)}) rotate(${(1 - p) * -5}deg)`;
        const hl = $('.hl', el);
        if (hl) hl.style.transform = `scaleX(${prog(t, at(l.at) + 0.08, 0.3, ease.outExpo)}) rotate(-2deg)`;
      });
      if (b.reveal) {
        const r = prog(t, at(b.reveal.at), 0.6, ease.outExpo);
        st.box.style.transform = `translateY(${-r * 90}px) scale(${1 - r * 0.22})`;
        st.box.style.opacity = 1 - r * 0.55;
        st.icon.style.translate = `0 ${-r * 40}px`;
        st.reveal.style.opacity = r;
        st.reveal.style.transform = `translateY(${(1 - r) * 70}px) scale(${lerp(0.9, 1, r)})`;
      }
    },
  };

  // Grande icône + phrase + sous-titre.
  BLOCKS.icon = {
    build(el, b) {
      el.insertAdjacentHTML('beforeend', `
        <div class="abs ic-halo"></div>
        <div class="abs ic-big" style="color:${col(b.color)}">${icon(b.icon)}</div>
        ${b.text ? `<div class="abs ic-text">${b.text}</div>` : ''}
        ${b.sub ? `<div class="abs ic-sub">${b.sub}</div>` : ''}`);
      return { halo: $('.ic-halo', el), big: $('.ic-big', el), text: $('.ic-text', el), sub: $('.ic-sub', el) };
    },
    render(t, b, st) {
      const p = prog(t, at(b.at), 0.7, ease.outElastic);
      popIn(st.big, p, -30);
      st.big.style.translate = `0 ${Math.sin(t * 2.5) * 10}px`;
      const h = prog(t, at(b.at), 0.9, ease.outExpo);
      st.halo.style.opacity = h * 0.9;
      st.halo.style.transform = `scale(${0.5 + h * 0.5 + Math.sin(t * 2) * 0.02})`;
      if (st.text) rise(st.text, prog(t, at(b.textAt || b.at) + 0.2, 0.7, ease.outExpo));
      if (st.sub) rise(st.sub, prog(t, at(b.subAt), 0.6, ease.outExpo), 40);
    },
  };

  // Grand compteur en plusieurs étapes, courbe et tampon.
  BLOCKS.counter = {
    build(el, b) {
      el.insertAdjacentHTML('beforeend', `
        <div class="abs panel" style="top:${b.top || 470}px">
          <div class="pl-lbl">${b.label || ''}</div>
          <div class="ct-big">0</div>
          <div class="ct-sub"></div>
          <svg class="ct-line" viewBox="0 0 960 300" preserveAspectRatio="none"><path fill="none" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><circle r="13" fill="#fff"/></svg>
          ${b.badge ? `<div class="badge ${b.badge.color || 'gold'}">${b.badge.text}<small>${b.badge.small || ''}</small></div>` : ''}
        </div>
        ${b.disclaimer ? `<div class="abs disc">${b.disclaimer}</div>` : ''}`);
      const path = $('.ct-line path', el);
      const vals = [b.from ?? 0, ...b.stages.map((s) => s.to)];
      const lo = Math.min(...vals), hi = Math.max(...vals);
      const y = (v) => lerp(260, 40, hi === lo ? 1 : (v - lo) / (hi - lo));
      // Courbe lissée passant par les étapes
      const pts = vals.map((v, i) => [lerp(40, 920, i / (vals.length - 1)), y(v)]);
      let d = `M${pts[0][0]} ${pts[0][1]}`;
      for (let i = 1; i < pts.length; i++) {
        const [x0, y0] = pts[i - 1], [x1, y1] = pts[i];
        d += ` C${(x0 + x1) / 2} ${y0} ${(x0 + x1) / 2} ${y1} ${x1} ${y1}`;
      }
      path.setAttribute('d', d);
      path.setAttribute('stroke', col(b.color));
      const len = path.getTotalLength();
      path.style.strokeDasharray = len;
      return { panel: $('.panel', el), big: $('.ct-big', el), sub: $('.ct-sub', el), path, len, dot: $('.ct-line circle', el), badge: $('.badge', el), disc: $('.disc', el), vals };
    },
    render(t, b, st) {
      const pp = prog(t, at(b.at || b.stages[0].at) - 0.5, 0.6, ease.outExpo);
      rise(st.panel, pp, 120);
      let v = b.from ?? 0, label = b.fromLabel || '', progress = 0;
      b.stages.forEach((s, i) => {
        const p = prog(t, at(s.at), s.dur || 0.9, ease.inOutCubic);
        if (p > 0) { v = lerp(st.vals[i], s.to, p); label = s.label || label; progress = (i + p) / b.stages.length; }
      });
      st.big.textContent = fmt(v, b.format);
      st.big.style.color = progress > 0.01 ? col(b.color) : 'var(--ink)';
      st.sub.textContent = label;
      st.path.style.strokeDashoffset = st.len * (1 - progress);
      const pt = st.path.getPointAtLength(Math.max(0.01, st.len * progress));
      st.dot.setAttribute('cx', pt.x); st.dot.setAttribute('cy', pt.y);
      st.dot.style.opacity = progress > 0.01 ? 1 : 0;
      if (st.badge) {
        const bp = prog(t, at(b.badge.at), 0.7, ease.outElastic);
        st.badge.style.opacity = clamp(bp * 3);
        st.badge.style.transform = `scale(${bp}) rotate(${-6 + (1 - bp) * 25}deg)`;
      }
      if (st.disc) st.disc.style.opacity = pp * 0.85;
    },
  };

  // Barres horizontales comparées.
  BLOCKS.bars = {
    build(el, b) {
      const max = b.max || Math.max(...b.items.map((i) => i.value));
      el.insertAdjacentHTML('beforeend', `
        <div class="abs panel" style="top:${b.top || 470}px; padding-top:40px">
          ${b.label ? `<div class="pl-lbl">${b.label}</div>` : ''}
          ${b.items.map((it) => `
            <div class="br-row">
              <div class="br-lbl">${it.label}${it.sub ? `<small>${it.sub}</small>` : ''}</div>
              <div class="br-track"><div class="br-bar" style="width:${(it.value / max) * 100}%; background:${col(it.color)}"></div></div>
              <div class="br-val" style="color:${col(it.color)}">0</div>
            </div>`).join('')}
          ${b.badge ? `<div class="badge ${b.badge.color || 'gold'}" style="right:40px; bottom:40px; top:auto">${b.badge.text}<small>${b.badge.small || ''}</small></div>` : ''}
        </div>`);
      return { panel: $('.panel', el), rows: [...el.querySelectorAll('.br-row')], badge: $('.badge', el) };
    },
    render(t, b, st) {
      rise(st.panel, prog(t, at(b.items[0].at) - 0.4, 0.6, ease.outExpo), 120);
      b.items.forEach((it, i) => {
        const p = prog(t, at(it.at), 0.9, ease.outCubic);
        const row = st.rows[i];
        rise(row, prog(t, at(it.at) - 0.2, 0.4, ease.outExpo), 30);
        $('.br-bar', row).style.transform = `scaleX(${p})`;
        $('.br-val', row).textContent = fmt(it.value * p, b.format);
      });
      if (st.badge) {
        const bp = prog(t, at(b.badge.at), 0.7, ease.outElastic);
        st.badge.style.opacity = clamp(bp * 3);
        st.badge.style.transform = `scale(${bp}) rotate(${-6 + (1 - bp) * 25}deg)`;
      }
    },
  };

  // Donut par parts, contenu central qui change.
  BLOCKS.donut = {
    build(el, b) {
      const R = 230, SW = 96, C = 2 * Math.PI * R;
      let acc = 0;
      const arcs = b.parts.map((p, i) => {
        const off = acc; acc += (p.pct / 100) * C;
        return `<circle data-i="${i}" cx="300" cy="300" r="${R}" fill="none" stroke="${col(p.color)}" stroke-width="${SW}" transform="rotate(-90 300 300)" stroke-dasharray="0 ${C}" stroke-dashoffset="${-off}"/>`;
      }).join('');
      el.insertAdjacentHTML('beforeend', `
        <svg class="abs dn" viewBox="0 0 600 600"><circle cx="300" cy="300" r="${R}" fill="none" stroke="rgba(243,238,228,0.06)" stroke-width="${SW}"/>${arcs}</svg>
        <div class="abs dn-center">
          ${b.parts.map((p) => `<div class="dn-slot"><div class="dn-pct" style="color:${col(p.color)}">${p.pct}&nbsp;%</div><div class="dn-lbl">${p.label}</div>${p.amount ? `<div class="dn-amt">${p.amount}</div>` : ''}</div>`).join('')}
          ${b.final ? `<div class="dn-slot"><div class="dn-pct" style="color:${col(b.final.color)}; font-size:96px">${b.final.big}</div><div class="dn-lbl">${b.final.small}</div></div>` : ''}
        </div>
        <div class="abs dn-legend">${b.parts.map((p) => `<span><i style="background:${col(p.color)}"></i>${p.label}</span>`).join('')}</div>`);
      return { svg: $('.dn', el), arcs: [...el.querySelectorAll('.dn circle[data-i]')], slots: [...el.querySelectorAll('.dn-slot')], legend: $('.dn-legend', el), R, C, SW };
    },
    render(t, b, st) {
      const sp = prog(t, at(b.parts[0].at) - 0.5, 0.9, ease.outExpo);
      st.svg.style.opacity = sp;
      st.svg.style.transform = `rotate(${(1 - sp) * -120}deg) scale(${0.7 + sp * 0.3})`;
      const fin = b.final ? prog(t, at(b.final.at), 0.5, ease.inOutCubic) : 0;
      b.parts.forEach((p, i) => {
        const ap = prog(t, at(p.at), 0.8, ease.inOutCubic);
        st.arcs[i].setAttribute('stroke-dasharray', `${Math.max(0, ((p.pct / 100) * st.C - 8) * ap)} ${st.C}`);
        const hi = b.final && b.final.highlight === i;
        st.arcs[i].setAttribute('stroke-width', st.SW + (hi ? fin * 30 : 0));
        st.arcs[i].style.opacity = hi || !b.final ? 1 : 1 - fin * 0.7;
        const next = b.parts[i + 1] ? at(b.parts[i + 1].at) : b.final ? at(b.final.at) : 1e9;
        const inP = prog(t, at(p.at) + 0.1, 0.45, ease.outBack);
        const outP = prog(t, next - 0.25, 0.3, ease.inCubic);
        st.slots[i].style.opacity = Math.min(clamp(inP * 2), 1 - outP);
        st.slots[i].style.transform = `scale(${0.6 + inP * 0.4 - outP * 0.3})`;
      });
      if (b.final) {
        const fp = prog(t, at(b.final.at) + 0.2, 0.6, ease.outBack);
        const f = st.slots[st.slots.length - 1];
        f.style.opacity = clamp(fp * 2);
        f.style.transform = `scale(${0.5 + fp * 0.5})`;
      }
      st.legend.style.opacity = prog(t, at(b.parts[b.parts.length - 1].at) + 0.4, 0.5);
    },
  };

  // Grille de cases qui se remplissent (semaines, mois…) + compteur.
  BLOCKS.grid = {
    build(el, b) {
      const cols = b.cols, rows = Math.ceil(b.cells / cols), gap = 10;
      const size = Math.floor((960 - gap * (cols - 1)) / cols);
      const cells = Array.from({ length: b.cells }, (_, i) =>
        `<div class="gd-cell" style="left:${(i % cols) * (size + gap)}px; top:${Math.floor(i / cols) * (size + gap)}px; width:${size}px; height:${size}px; font-size:${Math.round(size * 0.36)}px"><i></i><span>${i + 1}</span></div>`).join('');
      const h = rows * (size + gap);
      el.insertAdjacentHTML('beforeend', `
        <div class="abs gd" style="top:${b.top || 470}px; height:${h}px">${cells}</div>
        <div class="abs gd-count" style="top:${(b.top || 470) + h + 40}px">
          <div><div class="pl-lbl" style="position:static">${b.counter.label}</div><div class="gd-amt">0</div></div>
          ${b.badge ? `<div class="badge ${b.badge.color || 'gold'}" style="position:relative; right:auto; top:auto">${b.badge.text}<small>${b.badge.small || ''}</small></div>` : ''}
        </div>`);
      return { cells: [...el.querySelectorAll('.gd-cell')], amt: $('.gd-amt', el), count: $('.gd-count', el), badge: $('.badge', el) };
    },
    render(t, b, st) {
      // b.fill : [[jusqu'à la case n, début, fin], …]
      let filled = 0;
      const fillAt = [];
      let prev = 0;
      b.fill.forEach(([upTo, a, z]) => {
        for (let i = prev; i < upTo; i++) fillAt[i] = lerp(at(a), at(z), upTo - prev > 1 ? (i - prev) / (upTo - prev - 1) : 0);
        prev = upTo;
      });
      const appear = at(b.fill[0][1]) - 0.6;
      st.cells.forEach((c, i) => {
        const ap = prog(t, appear + (i / st.cells.length) * 0.5, 0.35, ease.outBack);
        c.style.opacity = clamp(ap * 2);
        c.style.transform = `scale(${ap})`;
        const fp = fillAt[i] !== undefined ? prog(t, fillAt[i], 0.25, ease.outBack) : 0;
        c.querySelector('i').style.transform = `scale(${fp})`;
        c.classList.toggle('on', fp > 0.5);
        if (fp >= 1) filled = i + 1;
      });
      const v = b.counter.mode === 'sum' ? (filled * (filled + 1)) / 2 * (b.counter.per || 1) : filled * (b.counter.per || 1);
      st.amt.textContent = fmt(v, b.format);
      rise(st.count, prog(t, appear + 0.3, 0.5, ease.outExpo), 40);
      if (st.badge) {
        const bp = prog(t, at(b.badge.at), 0.7, ease.outElastic);
        st.badge.style.opacity = clamp(bp * 3);
        st.badge.style.transform = `scale(${bp}) rotate(${-6 + (1 - bp) * 25}deg)`;
      }
    },
  };

  // Lignes (icône, libellé, montant) puis total en plusieurs étapes.
  BLOCKS.list = {
    build(el, b) {
      el.insertAdjacentHTML('beforeend', `
        <div class="abs ls" style="top:${b.top || 470}px">
          ${b.items.map((it) => `
            <div class="ls-row"><span class="ls-ic" style="color:${col(it.color)}">${icon(it.icon)}</span>
              <span class="ls-lbl">${it.label}${it.sub ? `<small>${it.sub}</small>` : ''}</span>
              <span class="ls-val" style="color:${col(it.color)}">${it.value}</span><i class="ls-strike"></i></div>`).join('')}
          ${b.total ? `<div class="ls-total"><span class="ls-tl">${b.total.label}</span><span class="ls-tv" style="color:${col(b.total.color)}">0</span></div>` : ''}
        </div>`);
      return { rows: [...el.querySelectorAll('.ls-row')], total: $('.ls-total', el), tv: $('.ls-tv', el), tl: $('.ls-tl', el) };
    },
    render(t, b, st) {
      b.items.forEach((it, i) => {
        const p = prog(t, at(it.at), 0.6, ease.outExpo);
        const row = st.rows[i];
        row.style.opacity = clamp(p * 2);
        row.style.transform = `translateX(${(1 - p) * -1100}px)`;
        if (b.strikeAt) $('.ls-strike', row).style.transform = `scaleX(${prog(t, at(b.strikeAt) + i * 0.15, 0.35, ease.outCubic)})`;
      });
      if (st.total) {
        const tp = prog(t, at(b.total.stages[0].at) - 0.2, 0.5, ease.outBack);
        st.total.style.opacity = clamp(tp * 2);
        st.total.style.transform = `scale(${tp})`;
        let v = 0, label = b.total.label, prev = 0;
        b.total.stages.forEach((s) => {
          const p = prog(t, at(s.at), s.dur || 0.7, ease.outCubic);
          if (p > 0) { v = lerp(prev, s.to, p); label = s.label || label; }
          prev = s.to;
        });
        st.tv.textContent = fmt(v, b.format);
        st.tl.textContent = label;
      }
    },
  };

  // Deux courbes de croissance comparées.
  BLOCKS.curves = {
    build(el, b) {
      const all = b.series.flatMap((s) => s.values.filter((v) => v !== null));
      const hi = Math.max(...all);
      const n = b.series[0].values.length;
      const X = (i) => lerp(60, 900, i / (n - 1)), Y = (v) => lerp(600, 120, v / hi);
      const paths = b.series.map((s, k) => {
        const pts = s.values.map((v, i) => (v === null ? null : [X(i), Y(v)])).filter(Boolean);
        return `<path data-k="${k}" d="${pts.map((p, i) => (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join(' ')}" fill="none" stroke="${col(s.color)}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>`;
      }).join('');
      const ticks = (b.xLabels || []).map((l, i, a) => `<text x="${lerp(60, 900, i / (a.length - 1))}" y="650" text-anchor="middle">${l}</text>`).join('');
      el.insertAdjacentHTML('beforeend', `
        <div class="abs panel" style="top:${b.top || 450}px; height:700px">
          <div class="pl-lbl">${b.label || ''}</div>
          <svg class="cv" viewBox="0 0 960 700"><line x1="60" x2="900" y1="600" y2="600" stroke="rgba(243,238,228,0.18)" stroke-width="2"/>${paths}<g class="cv-x">${ticks}</g></svg>
          ${b.series.map((s) => `<div class="cv-end" style="color:${col(s.color)}">${s.end.text}</div>`).join('')}
          ${b.badge ? `<div class="badge ${b.badge.color || 'gold'}" style="left:40px; right:auto; top:${b.badge.top || 150}px">${b.badge.text}<small>${b.badge.small || ''}</small></div>` : ''}
        </div>
        ${b.disclaimer ? `<div class="abs disc" style="top:${(b.top || 450) + 720}px">${b.disclaimer}</div>` : ''}`);
      const pathsEl = [...el.querySelectorAll('.cv path')];
      const ends = [...el.querySelectorAll('.cv-end')];
      pathsEl.forEach((p, k) => {
        const len = p.getTotalLength();
        p.style.strokeDasharray = len; p.dataset.len = len;
        const last = b.series[k].values.length - 1;
        // Étiquette : en légende (end.y donné) ou au bout de la courbe.
        const e = b.series[k].end;
        ends[k].style.left = (e.y !== undefined ? e.x ?? 50 : 500) + 'px';
        ends[k].style.top = (e.y !== undefined ? e.y : Y(b.series[k].values[last]) + (e.dy ?? -64)) + 'px';
      });
      return { panel: $('.panel', el), paths: pathsEl, ends, badge: $('.badge', el), disc: $('.disc', el) };
    },
    render(t, b, st) {
      rise(st.panel, prog(t, at(b.series[0].draw[0]) - 0.6, 0.6, ease.outExpo), 120);
      b.series.forEach((s, k) => {
        const p = prog(t, at(s.draw[0]), at(s.draw[1]) - at(s.draw[0]), ease.inOutCubic);
        st.paths[k].style.strokeDashoffset = st.paths[k].dataset.len * (1 - p);
        const ep = prog(t, at(s.end.at), 0.5, ease.outBack);
        st.ends[k].style.opacity = clamp(ep * 2);
        st.ends[k].style.transform = `translateX(${(1 - ep) * 40}px) scale(${ep})`;
      });
      if (st.badge) {
        const bp = prog(t, at(b.badge.at), 0.7, ease.outElastic);
        st.badge.style.opacity = clamp(bp * 3);
        st.badge.style.transform = `scale(${bp}) rotate(${-6 + (1 - bp) * 25}deg)`;
      }
      if (st.disc) st.disc.style.opacity = prog(t, at(b.series[0].draw[0]), 0.5) * 0.85;
    },
  };

  // Compte à rebours circulaire + jauge d'envie qui retombe.
  BLOCKS.timer = {
    build(el, b) {
      const R = 210, C = 2 * Math.PI * R;
      el.insertAdjacentHTML('beforeend', `
        <svg class="abs tm" viewBox="0 0 520 520"><circle cx="260" cy="260" r="${R}" fill="none" stroke="rgba(243,238,228,0.08)" stroke-width="34"/>
          <circle class="tm-arc" cx="260" cy="260" r="${R}" fill="none" stroke="var(--gold)" stroke-width="34" stroke-linecap="round" transform="rotate(-90 260 260)" stroke-dasharray="${C}" stroke-dashoffset="0"/></svg>
        <div class="abs tm-c"><div class="tm-ic">${icon(b.icon || 'cart')}</div><div class="tm-h">${b.hours} h</div></div>
        <div class="abs tm-meter"><div class="pl-lbl" style="position:static">${b.meterLabel || 'ENVIE D’ACHETER'}</div><div class="tm-track"><div class="tm-fill"></div></div></div>
        ${b.done ? `<div class="abs tm-done"><span>${b.done.text}</span></div>` : ''}`);
      return { svg: $('.tm', el), arc: $('.tm-arc', el), C, h: $('.tm-h', el), c: $('.tm-c', el), fill: $('.tm-fill', el), meter: $('.tm-meter', el), done: $('.tm-done', el) };
    },
    render(t, b, st) {
      const ap = prog(t, at(b.start) - 0.6, 0.6, ease.outBack);
      popIn(st.svg, ap); popIn(st.c, ap);
      rise(st.meter, prog(t, at(b.start) - 0.3, 0.5, ease.outExpo), 40);
      const p = prog(t, at(b.start), at(b.end) - at(b.start), ease.inOutCubic);
      st.arc.setAttribute('stroke-dashoffset', st.C * p);
      st.h.textContent = fmt(b.hours * (1 - p), 'h');
      const envie = lerp(1, 0.12, p);
      st.fill.style.transform = `scaleX(${envie})`;
      st.fill.style.background = envie > 0.5 ? 'var(--down)' : 'var(--up)';
      if (st.done) popIn(st.done, prog(t, at(b.done.at), 0.6, ease.outBack));
    },
  };

  // Étapes reliées par des flèches, une pièce qui descend.
  BLOCKS.steps = {
    build(el, b) {
      const top = b.top || 470, gap = 250;
      el.insertAdjacentHTML('beforeend', b.items.map((it, i) => `
        <div class="abs st-card" style="top:${top + i * gap}px; border-color:${it.color ? col(it.color) : ''}"><span class="st-ic" style="color:${col(it.color || 'gold')}">${icon(it.icon)}</span>
          <div><div class="st-l">${it.label}</div><div class="st-s">${it.sub || ''}</div></div></div>
        ${i < b.items.length - 1 ? `<div class="abs st-arrow" style="top:${top + i * gap + 186}px">↓</div>` : ''}`).join('') + `<div class="abs st-coin">€</div>`);
      return { cards: [...el.querySelectorAll('.st-card')], arrows: [...el.querySelectorAll('.st-arrow')], coin: $('.st-coin', el), top, gap };
    },
    render(t, b, st) {
      b.items.forEach((it, i) => {
        const p = prog(t, at(it.at), 0.6, ease.outBack);
        popIn(st.cards[i], p);
        if (st.arrows[i]) st.arrows[i].style.opacity = prog(t, at(b.items[i + 1].at) - 0.3, 0.3);
      });
      // La pièce descend de carte en carte, en boucle, après la dernière étape.
      const go = at(b.items[b.items.length - 1].at) + 0.5;
      if (t > go) {
        const u = ((t - go) / 1.6) % 1;
        const y = st.top + 70 + u * (b.items.length - 1) * st.gap;
        st.coin.style.opacity = Math.sin(u * Math.PI);
        st.coin.style.transform = `translate(${880}px, ${y}px) rotate(${u * 360}deg)`;
      } else st.coin.style.opacity = 0;
    },
  };

  // Appel à s'abonner + annonce de l'épisode suivant.
  BLOCKS.cta = {
    build(el, b) {
      el.insertAdjacentHTML('beforeend', `
        <div class="abs cta-ic">${icon('piggy')}</div>
        <h1 class="abs cta-title">${b.title || 'Abonne-<em>toi</em>'}</h1>
        <p class="abs cta-sub">${b.sub || 'pour ne rien rater'}</p>
        <div class="abs sub-btn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 22a2.5 2.5 0 0 0 2.45-2h-4.9A2.5 2.5 0 0 0 12 22Zm7-6V11a7 7 0 0 0-5.5-6.84V3.5a1.5 1.5 0 0 0-3 0v.66A7 7 0 0 0 5 11v5l-2 2v1h18v-1l-2-2Z"/></svg><span>S'ABONNER</span></div>
        <div class="abs ripple"></div><div class="abs finger"></div>
        <div class="abs handle">${EP.handle.replace(/^(@[^.]+)(\..*)?$/, '$1<span>$2</span>')}</div>
        ${EP.next ? `<div class="abs next"><div class="k">ÉPISODE ${String(EP.ep + 1).padStart(2, '0')}</div><div class="t">${EP.next}</div></div>` : ''}`);
      return { ic: $('.cta-ic', el), title: $('.cta-title', el), sub: $('.cta-sub', el), btn: $('.sub-btn', el), txt: $('.sub-btn span', el), rip: $('.ripple', el), finger: $('.finger', el), handle: $('.handle', el), next: $('.next', el) };
    },
    render(t, b, st) {
      const last = S[S.length - 1];
      const s = last.start;
      popIn(st.ic, prog(t, s - 0.2, 0.6, ease.outBack), -30);
      rise(st.title, prog(t, s, 0.6, ease.outExpo));
      st.sub.style.opacity = prog(t, s + 0.5, 0.5);
      const bp = prog(t, s + 0.3, 0.6, ease.outElastic);
      const tap = last.end + 0.4;
      const press = t > tap && t < tap + 0.25 ? Math.sin(((t - tap) / 0.25) * Math.PI) * 0.08 : 0;
      const breathe = t > s + 1 && t < tap ? Math.sin((t - s) * 7) * 0.03 : 0;
      st.btn.style.transform = `scale(${bp + breathe - press})`;
      st.btn.style.opacity = clamp(bp * 3);
      const done = t >= tap + 0.12;
      st.btn.classList.toggle('done', done);
      st.txt.textContent = done ? 'ABONNÉ ✓' : "S'ABONNER";
      const fp = prog(t, tap - 0.9, 0.8, ease.inOutCubic);
      st.finger.style.transform = `translate(${lerp(1100, 610, fp)}px, ${lerp(1250, 860, fp)}px) scale(${1 - press * 2})`;
      st.finger.style.opacity = fp > 0 ? 1 - prog(t, tap + 0.6, 0.4) : 0;
      const rp = prog(t, tap, 0.6);
      st.rip.style.transform = `translate(600px, 850px) scale(${0.3 + rp * 2.2})`;
      st.rip.style.opacity = t > tap ? 1 - rp : 0;
      rise(st.handle, prog(t, s + 0.8, 0.6, ease.outExpo), 30);
      if (st.next) rise(st.next, prog(t, last.end + 0.3, 0.7, ease.outExpo), 80);
    },
  };

  // ---------------------------------------------------------------- assemblage

  const segs = VO.segments.map((s) => ({ ...s, block: EP.blocks[s.name] }));
  const stage = document.getElementById('stage');
  stage.insertAdjacentHTML('beforeend', `
    <div class="abs topbar"><span><b>ÉPARGNE MALIN</b> · ÉP. ${String(EP.ep).padStart(2, '0')}</span><span>${EP.short || ''}</span></div>
    <div class="abs track"><i id="progress"></i></div>`);
  const capsLayer = html('<div class="abs cap" id="cap"></div>');

  // Sous-titres : pas pendant la 1re phrase quand le hook l'écrit déjà en grand.
  const hookFirst = segs[0].block && segs[0].block.type === 'hook';
  const caps = [];
  S.forEach((s, i) => s.chunks.forEach((c, j) => {
    const next = s.chunks[j + 1];
    if (!(i === 0 && hookFirst)) caps.push({ ...c, until: next ? next.start : s.end + 0.3 });
  }));

  M.scene({
    width: W, height: 1920, duration: VO.duration,
    setup() {
      segs.forEach((s) => {
        const b = s.block;
        if (!b) throw new Error('Pas de bloc pour le segment ' + s.name);
        const el = html(`<div class="seg"><div class="glow ${b.glow || 'gold'}"></div></div>`);
        if (b.chip) el.insertAdjacentHTML('beforeend', `<div class="abs chip ${b.chip.color || ''}">${b.chip.text}</div>`);
        if (b.title) el.insertAdjacentHTML('beforeend', `<h1 class="abs title">${b.title.html}</h1>`);
        stage.insertBefore(el, $('.topbar', stage));
        s.el = el;
        s.st = BLOCKS[b.type].build(el, b);
        s.chip = $('.chip', el);
        s.title = $('.title', el);
      });
      stage.insertBefore(capsLayer, $('.topbar', stage));
      return {};
    },
    render(t) {
      $('#progress').style.transform = `scaleX(${t / VO.duration})`;
      segs.forEach((s, k) => {
        const enter = k === 0 ? 1 : prog(t, s.start - 0.1, 0.5, ease.outExpo);
        const exit = k === segs.length - 1 ? 0 : prog(t, s.end - 0.12, 0.35, ease.inCubic);
        const on = enter > 0 && exit < 1;
        s.el.style.visibility = on ? 'visible' : 'hidden';
        if (!on) return;
        s.el.style.transform = `translateX(${(1 - enter) * 1000 - exit * 500}px) scale(${1 - exit * 0.08})`;
        s.el.style.opacity = 1 - exit;
        s.el.style.filter = enter < 1 || exit > 0 ? `blur(${(1 - enter) * 18 + exit * 18}px)` : 'none';
        const b = s.block;
        if (s.chip) popIn(s.chip, prog(t, at(b.chip.at), 0.45, ease.outBack));
        if (s.title) rise(s.title, prog(t, at(b.title.at), 0.7, ease.outExpo), 70);
        BLOCKS[b.type].render(t, b, s.st);
      });
      // Secousses de caméra
      let sh = 0;
      (EP.shakes || []).forEach((r) => {
        const a = at(r);
        if (t > a && t < a + 0.45) sh += (1 - (t - a) / 0.45) * 22;
      });
      stage.style.translate = `${Math.sin(t * 95) * sh}px ${Math.cos(t * 83) * sh}px`;

      // Sous-titres : un morceau à la fois, taille ajustée à la largeur.
      const cur = caps.find((k) => t >= k.start && t < k.until);
      if (!cur) { capsLayer.style.opacity = 0; return; }
      if (capsLayer.dataset.k !== String(cur.start)) {
        capsLayer.dataset.k = cur.start;
        capsLayer.innerHTML = '<span></span>';
        capsLayer.firstChild.textContent = cur.text;
        capsLayer.classList.toggle('gold', cur.gold);
        capsLayer.style.fontSize = '92px';
        // Largeur max 860 px (les morceaux dorés sont agrandis de 10 % et « rebondissent »).
        const w = capsLayer.firstChild.offsetWidth;
        if (w > 860) capsLayer.style.fontSize = Math.floor(92 * 860 / w) + 'px';
      }
      const p = prog(t, cur.start, 0.22, ease.outBack);
      const tilt = (Math.round(cur.start * 10) % 2 ? 1 : -1) * 1.5;
      capsLayer.style.opacity = clamp(p * 4);
      capsLayer.style.transform = `scale(${lerp(1.35, cur.gold ? 1.1 : 1, p)}) rotate(${tilt * (1 - p)}deg)`;
    },
  });
})();
