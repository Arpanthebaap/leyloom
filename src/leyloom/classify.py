"""Rule-based colour classifier. Mirrors the JavaScript in index.html (same thresholds, same priority)."""
import numpy as np

GROUPS = ("grass", "legume", "forb", "senescent", "bare")
DEFAULTS = {"hue_split": 98.0, "min_green": 0.22, "senescent": 0.30}


def rgb_to_hsv(rgb):
    """uint8 array (..., 3) -> hue (0-360), saturation, value (0-1)."""
    x = rgb.astype(np.float64) / 255.0
    r, g, b = x[..., 0], x[..., 1], x[..., 2]
    mx, mn = x.max(-1), x.min(-1)
    d = mx - mn
    nz = d > 0
    rm = nz & (mx == r)
    gm = nz & (mx == g) & ~rm
    bm = nz & ~rm & ~gm
    h = np.zeros_like(mx)
    h[rm] = ((g - b)[rm] / d[rm]) % 6
    h[gm] = (b - r)[gm] / d[gm] + 2
    h[bm] = (r - g)[bm] / d[bm] + 4
    h = (h * 60.0) % 360.0
    s = np.where(mx > 0, d / np.where(mx > 0, mx, 1.0), 0.0)
    return h, s, mx


def classify(rgb, hue_split=98.0, min_green=0.22, senescent=0.30):
    """Return an integer label per pixel: 0 grass, 1 legume, 2 forb, 3 senescent, 4 bare."""
    h, s, v = rgb_to_hsv(rgb)
    flower = ((v > .82) & (s < .14)) | ((s > .4) & (v > .5) & (((h >= 270) & (h <= 345)) | (h <= 12))) \
        | ((s > .7) & (v > .75) & (h >= 46) & (h <= 64))
    green = (h >= 65) & (h <= 170) & (s >= min_green) & (v > .12)
    sen = (h >= 28) & (h <= 65) & (s >= senescent) & (v > .3)
    lab = np.full(h.shape, 4, dtype=np.int8)
    lab[sen] = 3
    lab[green] = np.where(h[green] < hue_split, 0, 1)
    lab[flower] = 2
    return lab


def cover(labels):
    """Percent cover of the five classes, as a dict."""
    n = labels.size
    return {g: 100.0 * float((labels == i).sum()) / n for i, g in enumerate(GROUPS)}


def composition(c):
    """Grass, legume, forb as percent of their own sum (comparable with biomass fractions)."""
    t = c["grass"] + c["legume"] + c["forb"]
    return {k: (100.0 * c[k] / t if t else 0.0) for k in ("grass", "legume", "forb")}


def shannon(c):
    p = np.array([c["grass"], c["legume"], c["forb"]], dtype=float)
    t = p.sum()
    if t == 0:
        return 0.0
    p = p[p > 0] / t
    return float(-(p * np.log(p)).sum())
