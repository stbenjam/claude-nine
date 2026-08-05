#!/usr/bin/env node
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const manifestPath = process.argv[2];
if (!manifestPath) {
  console.error('Usage: render_movie_from_manifest.mjs <manifest.json>');
  process.exit(1);
}

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const root = path.dirname(path.resolve(manifestPath));
const framesDir = path.join(root, 'frames');
fs.mkdirSync(framesDir, { recursive: true });

function dataUrl(imagePath) {
  const absolute = path.resolve(root, imagePath);
  const ext = path.extname(absolute).toLowerCase().replace('.', '') || 'png';
  return `data:image/${ext === 'jpg' ? 'jpeg' : ext};base64,${fs.readFileSync(absolute).toString('base64')}`;
}

function htmlFor(slide, index) {
  const imageUrl = dataUrl(slide.image);
  const bullets = (slide.bullets || []).map((b) => `<li>${escapeHtml(b)}</li>`).join('');
  const color = slide.accentColor || '#0e7b5f';
  return `<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box} body{margin:0;width:1080px;height:1920px;overflow:hidden;font-family:"Noto Sans","DejaVu Sans",Arial,sans-serif;background:radial-gradient(circle at top left,${color}66,transparent 42%),linear-gradient(180deg,#11161a,#080a0d);color:white}.top{position:absolute;left:64px;right:64px;top:58px;display:flex;align-items:baseline;justify-content:space-between;gap:24px}.label{padding:14px 20px;border:2px solid rgba(255,255,255,.65);font-size:30px;text-transform:uppercase;background:rgba(0,0,0,.28)}.source{font-size:26px;color:rgba(255,255,255,.78);text-align:right}.shot{position:absolute;left:64px;right:64px;top:150px;height:1000px;border-radius:8px;overflow:hidden;border:6px solid rgba(255,255,255,.86);box-shadow:0 36px 90px rgba(0,0,0,.55);background:#fff}.shot img{width:100%;height:100%;object-fit:cover;object-position:${slide.cropPosition || 'top center'};display:block}.copy{position:absolute;left:64px;right:64px;top:1210px}h1{margin:0 0 10px;font-size:104px;line-height:.96;letter-spacing:0}.subtitle{font-size:42px;font-weight:760;color:#fff1d9;margin-bottom:34px}ul{list-style:none;margin:0;padding:0;display:grid;gap:18px}li{width:fit-content;max-width:920px;padding:18px 22px;background:rgba(255,255,255,.95);color:#111;font-size:37px;font-weight:760;line-height:1.14;border-radius:6px;border-left:12px solid ${color}}
</style></head><body><div class="top"><div class="label">${escapeHtml(slide.label || 'Screenshot')}</div><div class="source">${escapeHtml(manifest.subtitle || 'promo reel')}</div></div><div class="shot"><img src="${imageUrl}"></div><div class="copy"><h1>${escapeHtml(slide.title)}</h1><div class="subtitle">${escapeHtml(slide.subtitle || '')}</div><ul>${bullets}</ul></div></body></html>`;
}

function escapeHtml(value = '') {
  return String(value).replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
}

const browser = await chromium.launch({ headless: true, executablePath: manifest.chromiumPath || '/usr/bin/chromium-browser' });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
for (let i = 0; i < manifest.slides.length; i += 1) {
  const num = String(i + 1).padStart(2, '0');
  await page.setContent(htmlFor(manifest.slides[i], i), { waitUntil: 'load' });
  await page.screenshot({ path: path.join(framesDir, `slide-${num}.png`), fullPage: false });
}
await browser.close();
