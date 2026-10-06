#!/usr/bin/env node
/*
 * Exporte une scène en MP4, image par image.
 *
 *   node render.mjs scenes/01-intro-youtube.html            → videos/01-intro-youtube.mp4
 *   node render.mjs scenes/*.html                            → toutes les scènes
 *   node render.mjs scenes/02-interets-composes.html --still 4.5   → PNG à t = 4,5 s
 *   node render.mjs scenes/03-budget-50-30-20.html --fps 60
 *   node render.mjs scenes/05-short-30s.html --audio voix/30s-mix.wav   → MP4 avec le son
 *
 * Prérequis : Node 18+, ffmpeg dans le PATH, `npm install` dans ce dossier.
 */
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { basename, dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (name) => {
  const i = args.indexOf(name);
  if (i === -1) return undefined;
  const [, value] = args.splice(i, 2);
  return value;
};
const still = opt('--still');
const fpsArg = opt('--fps');
const audio = opt('--audio');
const outDir = resolve(opt('--out') ?? join(here, 'videos'));
const files = args;

if (!files.length) {
  console.error('Usage : node render.mjs <scene.html> [...] [--fps 30] [--still <secondes>] [--audio <fichier.wav>] [--out <dossier>]');
  process.exit(1);
}
mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch(
  process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {},
);

for (const file of files) {
  const name = basename(file, '.html');
  const page = await browser.newPage({ deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(resolve(file)).href + '?render=1');
  await page.waitForFunction(() => window.__motion);
  await page.evaluate(() => window.__motion.ready);
  const { width, height, duration, fps: sceneFps } = await page.evaluate(() => {
    const { width, height, duration, fps } = window.__motion;
    return { width, height, duration, fps };
  });
  await page.setViewportSize({ width, height });
  const fps = Number(fpsArg ?? sceneFps);

  if (still !== undefined) {
    await page.evaluate((t) => window.__motion.seek(t), Number(still));
    const out = join(outDir, `${name}@${still}s.png`);
    await page.screenshot({ path: out });
    console.log(`✓ ${out}`);
    await page.close();
    continue;
  }

  const out = join(outDir, `${name}.mp4`);
  const ffmpeg = spawn('ffmpeg', [
    '-y', '-loglevel', 'error',
    '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-',
    ...(audio ? ['-i', resolve(audio), '-c:a', 'aac', '-b:a', '192k', '-shortest'] : []),
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
    '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
    out,
  ], { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise((ok, ko) => ffmpeg.on('close', (code) => (code ? ko(new Error(`ffmpeg a échoué (${code})`)) : ok())));

  const total = Math.round(duration * fps);
  for (let i = 0; i <= total; i++) {
    await page.evaluate((t) => window.__motion.seek(t), i / fps);
    const png = await page.screenshot({ type: 'png' });
    if (!ffmpeg.stdin.write(png)) await new Promise((r) => ffmpeg.stdin.once('drain', r));
    process.stdout.write(`\r${name} : ${i}/${total} images`);
  }
  ffmpeg.stdin.end();
  await done;
  process.stdout.write(`\r✓ ${out} (${width}×${height}, ${duration} s, ${fps} i/s)\n`);
  await page.close();
}

await browser.close();
