const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.join(__dirname, '..', 'web', 'argent-maitrise.html'), { waitUntil: 'networkidle' });
  const r = await p.evaluate(() => {
    const txt = (sim, sel) => document.querySelectorAll('.sim')[sim].querySelector(sel)?.textContent.trim();
    return {
      precaution_cible: txt(0, '[data-o=cible]'),
      composes_final:   txt(1, '[data-o=fin]'),
      frais_faibles:    txt(2, '[data-o=a]'),
      frais_eleves:     txt(2, '[data-o=bb]'),
      locatif_cout:     txt(4, '[data-o=cout]'),
      locatif_mens:     txt(4, '[data-o=mens]'),
      locatif_cf:       txt(4, '[data-o=cf]'),
      locatif_rb:       txt(4, '[data-o=rb]'),
    };
  });
  console.log(JSON.stringify({ ...r, errors: errs }, null, 1));
  await b.close();
})();
