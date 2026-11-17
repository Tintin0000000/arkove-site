const { chromium } = require('playwright');
const path = require('path');

const BUILD = __dirname;

const FOOTER = `
<div style="width:100%;font-family:Inter,Helvetica,sans-serif;font-size:7.5px;color:#9a9race;
 padding:0 0.72in;display:flex;justify-content:space-between;align-items:center;">
  <span style="color:#A8A090;letter-spacing:0.08em;text-transform:uppercase;">Argent Maîtrisé</span>
  <span style="color:#17140F;font-weight:600;"><span class="pageNumber"></span></span>
</div>`.replace('#9a9race', '#A8A090');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Couverture : aucun en-tête ni pied de page
  await page.goto('file://' + path.join(BUILD, 'cover-court.html'), { waitUntil: 'load' });
  await page.pdf({
    path: path.join(BUILD, 'part-cover-court.pdf'),
    preferCSSPageSize: true,
    printBackground: true,
  });

  // Corps : pied de page numéroté
  await page.goto('file://' + path.join(BUILD, 'body-court.html'), { waitUntil: 'load' });
  await page.emulateMedia({ media: 'print' });
  const opts = {
    path: path.join(BUILD, 'part-body-court.pdf'),
    preferCSSPageSize: true,
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: FOOTER,
  };
  try {
    await page.pdf({ ...opts, outline: true, tagged: true });
    console.log('corps généré (avec signets PDF)');
  } catch (e) {
    await page.pdf(opts);
    console.log('corps généré (sans signets) :', e.message.split('\n')[0]);
  }

  await browser.close();
})();
