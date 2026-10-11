#!/usr/bin/env node
// Couvertures du profil TikTok : une image 1080×1920 par épisode (serie/couvertures/epNN.png).
// Le texte reste dans la zone visible de la grille du profil (environ y 240 → 1680).
//   node serie/covers.mjs
import { chromium } from 'playwright';
import { readFileSync, readdirSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const out = join(here, 'couvertures');
mkdirSync(out, { recursive: true });

// Les icônes sont celles de serie.js.
const src = readFileSync(join(here, 'serie.js'), 'utf8');
const ICONS = eval('(' + src.slice(src.indexOf('const ICONS = {') + 14, src.indexOf('};', src.indexOf('const ICONS = {')) + 1) + ')');
const icon = (n) => `<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">${ICONS[n]}</svg>`;

const eps = [JSON.parse(readFileSync(join(here, 'ep01-post.json'), 'utf8'))]
  .concat(readdirSync(here).filter((f) => /^ep\d\d\.json$/.test(f)).sort().map((f) => JSON.parse(readFileSync(join(here, f), 'utf8'))));

const page = (e) => `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
  @font-face { font-family: 'Inter Tight'; src: url(../../fonts/InterTight-Variable.woff2); font-weight: 100 900; }
  @font-face { font-family: 'Instrument Serif'; src: url(../../fonts/InstrumentSerif-Italic.woff2); font-style: italic; }
  @font-face { font-family: 'JetBrains Mono'; src: url(../../fonts/JetBrainsMono-Variable.woff2); font-weight: 100 800; }
  html, body { margin: 0; width: 1080px; height: 1920px; background: #0d0c0a; color: #f3eee4; overflow: hidden; }
  .bg { position: absolute; inset: 0; background:
      radial-gradient(circle at 50% 46%, rgba(206,155,76,0.30), transparent 55%),
      linear-gradient(rgba(243,238,228,0.06) 1px, transparent 1px) 0 0 / 90px 90px,
      linear-gradient(90deg, rgba(243,238,228,0.06) 1px, transparent 1px) 0 0 / 90px 90px; }
  .wrap { position: absolute; left: 70px; right: 70px; top: 300px; bottom: 300px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 44px; text-align: center; }
  .ep { font: 700 36px 'JetBrains Mono', monospace; letter-spacing: 0.24em; color: #0d0c0a; background: #e8c27a; padding: 14px 30px; border-radius: 999px; }
  .ic { width: 230px; height: 230px; color: #e8c27a; }
  .k { font: 900 132px/0.98 'Inter Tight', sans-serif; letter-spacing: -0.045em; text-transform: uppercase; text-wrap: balance; }
  .t { font: italic 400 96px/1 'Instrument Serif', serif; color: #e8c27a; text-wrap: balance; }
  .h { position: absolute; left: 0; right: 0; bottom: 320px; text-align: center; font: 700 34px 'JetBrains Mono', monospace; letter-spacing: 0.16em; color: #a79c88; }
</style></head><body><div class="bg"></div>
  <div class="wrap"><div class="ep">ÉPISODE ${String(e.ep).padStart(2, '0')}</div><div class="ic">${icon(e.cover.icon)}</div>
  <div class="k" id="k">${e.cover.kicker.replace(/ ([:?!;])/g, "\u00a0$1")}</div><div class="t">${e.title}</div></div>
  <div class="h">${(e.handle || "@epargne.malin7").toUpperCase()}</div></body></html>`;

const browser = await chromium.launch();
const tab = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
const tmp = join(out, '.tmp.html');
for (const e of eps) {
  writeFileSync(tmp, page(e));
  await tab.goto(pathToFileURL(tmp).href);
  await tab.evaluate(async () => {
    await document.fonts.ready;
    const k = document.getElementById('k');                 // le titre choc tient sur 3 lignes max
    let fs = 132;
    while (k.offsetHeight > 3 * fs * 1.0 + 10 && fs > 70) { fs -= 4; k.style.fontSize = fs + 'px'; }
  });
  await tab.screenshot({ path: join(out, `ep${String(e.ep).padStart(2, '0')}.png`) });
  console.log('✓ couverture', e.ep);
}
rmSync(tmp);
await browser.close();
