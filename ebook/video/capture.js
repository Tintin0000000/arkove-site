const { chromium } = require('playwright');
const path = require('path');
const FPS = 24, DUR = 27, OUT = process.argv[2];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(__dirname, 'scene1.html'), { waitUntil: 'networkidle' });
  await p.waitForFunction(() => window.__ready === true, null, { timeout: 15000 });
  const total = FPS * DUR;
  for (let i = 0; i < total; i++) {
    await p.evaluate((t) => window.render(t), i / FPS);
    await p.screenshot({ path: path.join(OUT, String(i).padStart(4, '0') + '.jpg'),
                         type: 'jpeg', quality: 92 });
    if (i % 150 === 0) process.stdout.write(`  ${i}/${total}\n`);
  }
  console.log(`${total} images capturées`);
  await b.close();
})();
