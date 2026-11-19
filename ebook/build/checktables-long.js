const { chromium } = require('playwright');
const path = require('path');
// Hauteur utile d'une page : 9in - marges (0.66 haut + 0.76 bas) = 7.58in à 96 dpi
const PAGE_PX = (9 - 0.78 - 0.86) * 96;

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: Math.round(6 * 96), height: 900 } });
  await p.goto('file://' + path.join(__dirname, 'body.html'), { waitUntil: 'load' });
  await p.emulateMedia({ media: 'print' });
  const r = await p.evaluate((limit) => {
    const grab = (sel) => [...document.querySelectorAll(sel)].map((el, i) => ({
      i, h: Math.round(el.getBoundingClientRect().height),
      t: (el.querySelector('th')?.textContent || el.textContent || '').trim().slice(0, 48),
    }));
    const tables = grab('table'), figs = grab('figure.figure'), boxes = grab('div.encadre,div.alerte,div.action,div.exemple');
    return {
      limitPx: Math.round(limit),
      tables: { n: tables.length, max: Math.max(...tables.map(x => x.h)), over: tables.filter(x => x.h > limit) },
      figures: { n: figs.length, max: Math.max(...figs.map(x => x.h)), over: figs.filter(x => x.h > limit) },
      encadres: { n: boxes.length, max: Math.max(...boxes.map(x => x.h)), over: boxes.filter(x => x.h > limit) },
    };
  }, PAGE_PX);
  console.log(JSON.stringify(r, null, 1));
  await b.close();
})();
