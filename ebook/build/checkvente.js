const { chromium } = require('playwright');
const path = require('path');
const URL = 'file://' + path.join(__dirname, '..', 'web', 'vente.html');
(async () => {
  const b = await chromium.launch();
  const errs = [];
  const p = await b.newPage({ viewport: { width: 1280, height: 900 }, colorScheme: 'light' });
  p.on('pageerror', e => errs.push(e.message));
  await p.goto(URL, { waitUntil: 'networkidle' });
  await p.screenshot({ path: 'build/v-top.png' });
  await p.evaluate(() => document.getElementById('offre').scrollIntoView({ block: 'start' }));
  await p.waitForTimeout(300);
  await p.screenshot({ path: 'build/v-offre.png' });
  const ovD = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);

  const m = await b.newPage({ viewport: { width: 390, height: 800 }, colorScheme: 'dark', deviceScaleFactor: 2 });
  await m.goto(URL, { waitUntil: 'networkidle' });
  await m.evaluate(() => document.querySelector('.demo').scrollIntoView({ block: 'center' }));
  await m.waitForTimeout(300);
  await m.screenshot({ path: 'build/v-mobile.png' });
  const ovM = await m.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);

  console.log(JSON.stringify({
    overflowDesktop: ovD, overflowMobile: ovM, errors: errs,
    aCompleter: await p.evaluate(() => document.querySelectorAll('.todo').length),
    simulateur: await p.evaluate(() => document.getElementById('o-t').textContent),
  }));
  await b.close();
})();
