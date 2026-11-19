const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 800, height: 1280 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'cover.html'), { waitUntil: 'networkidle' });
  await p.locator('.c').screenshot({ path: path.join(__dirname, 'couverture-kindle.png') });
  console.log('couverture rendue');
  await b.close();
})();
