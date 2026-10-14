#!/usr/bin/env python3
"""Convert GrassClover biomass annotations to Leyloom benchmark reference CSV.

Outputs data/reference.csv with columns:
  image,grass,legume,forb,site

Assumptions:
1. Weeds -> Forb:
   In GrassClover organic trial plots, weeds are broadleaf non-legume herbaceous plants
   (dicots such as dandelion, dock, thistle, etc.). In Leyloom's functional-group schema,
   these correspond botanically to the 'forb' functional group.
2. Clover -> Legume:
   Both white clover (Trifolium repens) and red clover (Trifolium pratense) are
   fabaceous forage legumes and map to Leyloom's 'legume' class.
3. Grass -> Grass:
   Grass biomass maps directly to Leyloom's 'grass' class.
4. Percentages sum to 100:
   dry_grass_fraction + dry_clover_fraction + dry_weeds_fraction sum to 1.0 in GrassClover.
   Values are converted to percent (0-100) and normalized by their sum.
5. Site mapping (Acquisition System):
   Images were captured using two distinct physical camera systems identified via EXIF:
   - NIKON_D810A (142 images)
   - ILCE-7 (Sony Alpha 7, 119 images)
   These provide realistic non-overlapping clusters for cross-site/cross-sensor validation.
"""
import argparse
import os
import sys
import pandas as pd
from PIL import Image


def get_camera_system(img_path):
    """Extract camera model from EXIF metadata."""
    try:
        with Image.open(img_path) as im:
            ex = im._getexif() or {}
            # Tag 272 is Model
            model = ex.get(272, "Unknown").strip()
            return model.replace(" ", "_")
    except Exception:
        return "Unknown"


def main():
    parser = argparse.ArgumentParser(description="Prepare GrassClover reference CSV for Leyloom")
    parser.add_argument("--images", default="data/images", help="Path to images directory")
    parser.add_argument("--labels", default="data/images/biomass_train_data.csv", help="Path to GrassClover CSV")
    parser.add_argument("--out", default="data/reference.csv", help="Output reference CSV path")
    args = parser.parse_args()

    if not os.path.exists(args.labels):
        sys.exit(f"Labels file not found: {args.labels}")

    df = pd.read_csv(args.labels, sep=";")
    print(f"Loaded {len(df)} rows from {args.labels}")

    rows = []
    for _, r in df.iterrows():
        img_name = str(r["image_file_name"]).strip()
        img_path = os.path.join(args.images, img_name)
        if not os.path.exists(img_path):
            print(f"Warning: image {img_name} not found in {args.images}, skipping")
            continue

        camera = get_camera_system(img_path)

        # Dry fractions
        g_frac = float(r["dry_grass_fraction"])
        l_frac = float(r["dry_clover_fraction"])
        f_frac = float(r["dry_weeds_fraction"])

        total = g_frac + l_frac + f_frac
        if total <= 0:
            print(f"Warning: zero total fraction for {img_name}, skipping")
            continue

        # Scale to percent of three-group sum
        g_pct = round(100.0 * g_frac / total, 3)
        l_pct = round(100.0 * l_frac / total, 3)
        f_pct = round(100.0 * f_frac / total, 3)

        rows.append({
            "image": img_name,
            "grass": g_pct,
            "legume": l_pct,
            "forb": f_pct,
            "site": camera
        })

    out_df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    out_df.to_csv(args.out, index=False)
    print(f"Wrote {len(out_df)} reference samples to {args.out}")
    print("\nSummary by site (camera system):")
    print(out_df["site"].value_counts().to_string())
    print("\nSample rows:")
    print(out_df.head().to_string(index=False))


if __name__ == "__main__":
    main()
