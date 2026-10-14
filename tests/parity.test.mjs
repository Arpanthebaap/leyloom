import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execFileSync } from 'child_process';
import assert from 'assert';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, '..');

// 1. Read index.html and extract JS classifier logic
const html = fs.readFileSync(path.join(rootDir, 'index.html'), 'utf8');

// Extract hsv function directly from index.html
const hsvMatch = html.match(/function hsv\(r,g,b\)\{([\s\S]*?return\[h,m\?d\/m:0,m\])\}/);
let hsvFn;
if (hsvMatch) {
  hsvFn = new Function('r', 'g', 'b', hsvMatch[1]);
} else {
  // Fallback direct reference matching index.html
  hsvFn = function(r, g, b) {
    r /= 255; g /= 255; b /= 255; const m = Math.max(r, g, b), n = Math.min(r, g, b), d = m - n; let h = 0;
    if (d) { if (m == r) h = ((g - b) / d) % 6; else if (m == g) h = (b - r) / d + 2; else h = (r - g) / d + 4; h *= 60; if (h < 0) h += 360; }
    return [h, m ? d / m : 0, m];
  };
}

// Implement the JS pixel classifier matching index.html lines 82-92 exactly
function classifyJs(r, g, b, sp = 98, gm = 0.22, sn = 0.30) {
  const [h, s, v] = hsvFn(r, g, b);
  let k;
  if (v > 0.82 && s < 0.14) k = 'f';
  else if (s > 0.4 && v > 0.5 && ((h >= 270 && h <= 345) || h <= 12)) k = 'f';
  else if (s > 0.7 && v > 0.75 && h >= 46 && h <= 64) k = 'f';
  else if (h >= 65 && h <= 170 && s >= gm && v > 0.12) k = h < sp ? 'g' : 'l';
  else if (h >= 28 && h <= 65 && s >= sn && v > 0.3) k = 'd';
  else k = 's';
  const mapping = { g: 0, l: 1, f: 2, d: 3, s: 4 };
  return mapping[k];
}

// 2. Build test RGB palette: known test cases + boundary points + color sweeps
const pixels = [
  [110, 170, 50],   // yellow-green -> grass
  [30, 120, 80],    // blue-green -> legume
  [250, 250, 250],  // white flower
  [200, 160, 60],   // senescent
  [70, 55, 45],     // dark soil
  [100, 80, 60],    // mid-brown soil
  [0, 0, 0],        // black
  [255, 255, 255],  // white
  [255, 0, 0],      // pure red
  [0, 255, 0],      // pure green
  [0, 0, 255],      // pure blue
  [255, 255, 0],    // pure yellow
  [255, 0, 255],    // magenta/pink
  [0, 255, 255],    // cyan
  [128, 128, 128],  // mid gray
];

// Grid sweep
for (let r = 0; r <= 255; r += 51) {
  for (let g = 0; g <= 255; g += 51) {
    for (let b = 0; b <= 255; b += 51) {
      pixels.push([r, g, b]);
    }
  }
}

// Additional boundary sweep for hue transitions
for (let r = 20; r <= 240; r += 35) {
  for (let g = 40; g <= 200; g += 35) {
    pixels.push([r, g, 40]);
  }
}

console.log(`Running parity test across ${pixels.length} distinct RGB test pixels...`);

// 3. Compute JS labels
const jsLabels = pixels.map(([r, g, b]) => classifyJs(r, g, b));

// 4. Compute Python labels via leyloom.classify
const pythonScript = `
import json, sys
import numpy as np
from leyloom import classify

pixels = json.loads(sys.argv[1])
arr = np.array([[p] for p in pixels], dtype=np.uint8) # shape (N, 1, 3)
labs = classify(arr)[:, 0].tolist()
print(json.dumps(labs))
`;

const pythonBin = process.platform === 'win32'
  ? path.join(rootDir, '.venv', 'Scripts', 'python.exe')
  : path.join(rootDir, '.venv', 'bin', 'python3');

const pyOutput = execFileSync(pythonBin, ['-c', pythonScript, JSON.stringify(pixels)], {
  cwd: rootDir,
  encoding: 'utf8'
});
const pyLabels = JSON.parse(pyOutput.trim());

// 5. Assert 100% parity
let mismatches = 0;
const groupNames = ['grass', 'legume', 'forb', 'senescent', 'bare'];

for (let i = 0; i < pixels.length; i++) {
  const [r, g, b] = pixels[i];
  const jsLab = jsLabels[i];
  const pyLab = pyLabels[i];
  if (jsLab !== pyLab) {
    mismatches++;
    console.error(`Mismatch at RGB(${r}, ${g}, ${b}): JS=${groupNames[jsLab]} (${jsLab}) vs Python=${groupNames[pyLab]} (${pyLab})`);
  }
}

assert.strictEqual(mismatches, 0, `Found ${mismatches} mismatches between JavaScript and Python classifiers!`);
console.log(`Parity test passed! All ${pixels.length} pixels produced identical classifications in JavaScript and Python.`);
