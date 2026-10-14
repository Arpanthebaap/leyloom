#!/usr/bin/env python3
"""Benchmark Leyloom against reference botanical composition.

Reference CSV columns: image,grass,legume,forb[,site]   (values are percent of the three-group total)
Example:
  python benchmark/run_benchmark.py --images data/images --reference data/reference.csv \
      --calibrate --test-sites siteC,siteD --out results/
With --calibrate, thresholds are fitted on images from sites NOT in --test-sites, then applied to the held-out sites.
"""
import argparse, json, os, sys
import numpy as np, pandas as pd
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from leyloom import classify, cover, composition, summary, calibrate, DEFAULTS


def load(path, width):
    im = Image.open(path).convert("RGB")
    im = im.resize((width, max(1, round(im.height * width / im.width))))
    return np.asarray(im)


def predict(imgs, params):
    return np.array([[composition(cover(classify(i, **params)))[k] for k in ("grass", "legume", "forb")] for i in imgs])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", required=True); ap.add_argument("--reference", required=True)
    ap.add_argument("--width", type=int, default=400); ap.add_argument("--out", default="results")
    ap.add_argument("--calibrate", action="store_true"); ap.add_argument("--test-sites", default="")
    a = ap.parse_args()
    df = pd.read_csv(a.reference)
    imgs = [load(os.path.join(a.images, f), a.width) for f in df["image"]]
    ref = df[["grass", "legume", "forb"]].to_numpy(float)
    if a.calibrate:
        if "site" not in df or not a.test_sites:
            sys.exit("--calibrate needs a 'site' column and --test-sites to avoid tuning on test data")
        test = df["site"].astype(str).isin(a.test_sites.split(",")).to_numpy()
        best, _ = calibrate([i for i, t in zip(imgs, test) if not t], ref[~test])
    else:
        test, best = np.ones(len(df), bool), None
    os.makedirs(a.out, exist_ok=True)
    rows, ti = [], [i for i, t in zip(imgs, test) if t]
    for name, params in [("default", DEFAULTS)] + ([("calibrated", best)] if best else []):
        pr = predict(ti, params)
        for j, k in enumerate(("grass", "legume", "forb")):
            rows.append({"thresholds": name, "group": k, **summary(pr[:, j], ref[test][:, j])})
    res = pd.DataFrame(rows).round(3)
    res.to_csv(os.path.join(a.out, "metrics.csv"), index=False)
    open(os.path.join(a.out, "metrics.md"), "w").write(res.to_markdown(index=False) if hasattr(res, "to_markdown") else res.to_string(index=False))
    json.dump({"calibrated_params": best, "n_test": int(test.sum())}, open(os.path.join(a.out, "run.json"), "w"), indent=2)
    print(res.to_string(index=False))


if __name__ == "__main__":
    main()
