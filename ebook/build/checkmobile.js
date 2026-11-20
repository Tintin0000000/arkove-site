const { chromium } = require('playwright');
const path = require('path');
const CONTENT_PX = Math.round((4.5 - 0.36 - 0.36) * 96);  // largeur utile de la page
const H = (8 - 0.42 - 0.52) * 96;
(async () => {
  const b = await chromium.launch();
  // viewport = largeur utile, pour que width:100% corresponde à la vraie colonne
  const p = await b.newPage({ viewport: { width: CONTENT_PX, height: 900 } });
  await p.goto('file://' + path.join(__dirname, 'body-mobile.html'), { waitUntil: 'load' });
  await p.emulateMedia({ media: 'print' });
  const r = await p.evaluate((h) => {
    const over = [];
    const check = (sel, kind) => document.querySelectorAll(sel).forEach((el) => {
      // débordement réel : le contenu ne tient pas dans sa propre boîte
      if (el.scrollWidth > el.clientWidth + 1) {
        over.push({ kind, debord: el.scrollWidth - el.clientWidth,
                    t: (el.querySelector('th')?.textContent || el.textContent || '').trim().slice(0, 38) });
      }
    });
    check('table', 'tableau'); check('div.formule', 'formule'); check('pre', 'code');
    const haut = [...document.querySelectorAll('table,figure.figure,div.encadre,div.alerte,div.action,div.exemple')]
      .filter(el => el.getBoundingClientRect().height > h)
      .map(el => ({ h: Math.round(el.getBoundingClientRect().height),
                    t: (el.textContent || '').trim().slice(0, 38) }));
    return { largeurColonne: document.body.clientWidth, debordements: over, tropHaut: haut };
  }, H);
  console.log(JSON.stringify(r, null, 1));
  await b.close();
})();
