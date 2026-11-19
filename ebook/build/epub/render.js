const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 980, height: 800 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'figs.html'), { waitUntil: 'load' });
  const n = await p.evaluate(() => document.querySelectorAll('.box').length);
  for (let i = 0; i < n; i++) {
    await p.locator('#f' + i).screenshot({ path: path.join(__dirname, 'img', `figure-${i + 1}.png`) });
  }
  console.log(n + ' figures rendues en PNG');
  await b.close();
})();
