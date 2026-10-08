#!/usr/bin/env node
// Exporte les SVG du logo en PNG (fond transparent quand le SVG n'a pas de fond).
//   node brand/export.mjs
import { chromium } from 'playwright';
import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const sizes = { 'avatar.svg': [1024, 400, 200], 'avatar-or.svg': [1024, 400, 200], 'avatar-creme.svg': [1024, 400, 200], 'avatar-nom.svg': [1024, 400], 'avatar-nom-or.svg': [1024, 400], 'avatar-nom-creme.svg': [1024, 400], 'icone.svg': [1024, 512] };

const browser = await chromium.launch();
const page = await browser.newPage();
for (const file of readdirSync(here).filter((f) => f.endsWith('.svg'))) {
  const svg = readFileSync(join(here, file), 'utf8');
  const [, w, h] = svg.match(/viewBox="0 0 (\d+) (\d+)"/).map(Number);
  for (const size of sizes[file] || [w]) {
    const scale = size / w;
    await page.setViewportSize({ width: Math.round(w * scale), height: Math.round(h * scale) });
    await page.setContent(`<style>html,body{margin:0;background:transparent}svg{display:block;width:100vw;height:100vh}</style>${svg}`);
    const out = join(here, file.replace('.svg', size === w ? '.png' : `-${size}.png`));
    await page.screenshot({ path: out, omitBackground: true });
    console.log('✓', out.split('/').pop());
  }
}
await browser.close();
