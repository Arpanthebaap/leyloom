import numpy as np
from leyloom import classify, cover, composition, shannon, summary, lins_ccc, calibrate, GROUPS

def px(r, g, b): return np.array([[[r, g, b]]], dtype=np.uint8)

def test_pixel_classes():
    assert classify(px(110, 170, 50))[0, 0] == 0      # yellow-green -> grass
    assert classify(px(30, 120, 80))[0, 0] == 1       # blue-green -> legume
    assert classify(px(250, 250, 250))[0, 0] == 2     # white flower
    assert classify(px(200, 160, 60))[0, 0] == 3      # senescent
    assert classify(px(70, 55, 45))[0, 0] == 4        # dark soil
    # known limitation: mid-brown soil (100, 80, 60) is labelled senescent by the colour rules
    assert classify(px(100, 80, 60))[0, 0] == 3

def test_cover_sums_to_100():
    img = np.random.default_rng(0).integers(0, 255, (50, 50, 3), dtype=np.uint8)
    assert abs(sum(cover(classify(img)).values()) - 100) < 1e-9

def test_shannon_bounds():
    assert shannon({"grass": 100, "legume": 0, "forb": 0}) == 0
    assert abs(shannon({"grass": 1, "legume": 1, "forb": 1}) - np.log(3)) < 1e-9

def test_metrics():
    x = np.array([10., 20, 30, 40])
    s = summary(x, x)
    assert s["mae"] == 0 and abs(s["ccc"] - 1) < 1e-9
    assert summary(x + 5, x)["bias"] == 5

def _img(h_grass, h_leg, frac, n=60):
    import colorsys
    g = [int(c * 255) for c in colorsys.hsv_to_rgb(h_grass / 360, .7, .6)]
    l = [int(c * 255) for c in colorsys.hsv_to_rgb(h_leg / 360, .7, .4)]
    a = np.zeros((n, n, 3), np.uint8); k = int(n * frac)
    a[:, :k] = l; a[:, k:] = g
    return a

def test_calibration_recovers_shifted_hues():
    imgs = [_img(112, 150, f) for f in (.1, .3, .5, .7)]
    ref = np.array([[100 * (1 - f), 100 * f, 0] for f in (.1, .3, .5, .7)])
    err_default = np.mean([abs(composition(cover(classify(i)))["legume"] - r[1]) for i, r in zip(imgs, ref)])
    best, ranked = calibrate(imgs, ref)
    assert 112 <= best["hue_split"] <= 150
    assert ranked[0][0] < err_default
