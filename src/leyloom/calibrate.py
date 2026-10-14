"""Threshold calibration by grid search. Fit on training sites only; report on held-out sites."""
import itertools
import numpy as np
from .classify import classify, cover, composition

GRID = {"hue_split": range(80, 131, 5), "min_green": (0.12, 0.17, 0.22, 0.27, 0.32), "senescent": (0.20, 0.30, 0.40)}


def _err(images, ref, params):
    errs = []
    for img, r in zip(images, ref):
        c = composition(cover(classify(img, **params)))
        errs.append([abs(c["grass"] - r[0]), abs(c["legume"] - r[1]), abs(c["forb"] - r[2])])
    return float(np.mean(errs))


def calibrate(images, ref, grid=None):
    """images: list of uint8 RGB arrays; ref: (n, 3) array of grass, legume, forb percent composition.
    Returns (best_params, ranked list of (mean absolute error, params))."""
    grid = grid or GRID
    keys = list(grid)
    out = []
    for vals in itertools.product(*[grid[k] for k in keys]):
        p = dict(zip(keys, vals))
        out.append((_err(images, ref, p), p))
    out.sort(key=lambda t: t[0])
    return out[0][1], out
