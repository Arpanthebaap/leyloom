"""Agreement statistics for comparing predicted and reference cover."""
import numpy as np


def mae(p, r): return float(np.mean(np.abs(np.asarray(p, float) - np.asarray(r, float))))
def rmse(p, r): return float(np.sqrt(np.mean((np.asarray(p, float) - np.asarray(r, float)) ** 2)))
def bias(p, r): return float(np.mean(np.asarray(p, float) - np.asarray(r, float)))


def lins_ccc(p, r):
    """Lin's concordance correlation coefficient (population variances)."""
    p, r = np.asarray(p, float), np.asarray(r, float)
    den = p.var() + r.var() + (p.mean() - r.mean()) ** 2
    return float(2 * np.mean((p - p.mean()) * (r - r.mean())) / den) if den else float("nan")


def bland_altman(p, r):
    """Mean difference and 95% limits of agreement."""
    d = np.asarray(p, float) - np.asarray(r, float)
    m, s = d.mean(), d.std(ddof=1) if len(d) > 1 else 0.0
    return {"bias": float(m), "loa_low": float(m - 1.96 * s), "loa_high": float(m + 1.96 * s)}


def summary(p, r):
    ba = bland_altman(p, r)
    return {"n": len(p), "mae": mae(p, r), "rmse": rmse(p, r), "bias": ba["bias"],
            "ccc": lins_ccc(p, r), "loa_low": ba["loa_low"], "loa_high": ba["loa_high"]}
