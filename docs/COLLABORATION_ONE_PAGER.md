# Leyloom: Research Collaboration One-Pager

## The Problem
Assessing botanical composition in perennial grass-clover and species-rich leys is critical for evaluating yield, nutritive value, and sward persistence. However, botanical hand-separation of harvested biomass is too slow for large-scale plot networks, while visual cover estimates vary substantially between human observers. Automated image analysis could enable rapid, repeatable monitoring, but field agronomists need transparent baselines with known error limits before trusting computer vision estimates.

## What Leyloom Does
Leyloom is an open-source, offline research tool and Python evaluation framework:
- **In-browser app (`index.html`):** Classifies pixels of a top-down quadrat photo into grass, legume, forb (flowers), senescent material, and bare ground using rule-based colour thresholds. Runs completely client-side (no data upload required).
- **Python package (`leyloom`):** Provides automated threshold calibration, functional-group diversity metrics (Shannon $H'$), and statistical validation against ground-truth reference data.
- **Inspectable baseline:** Operates with explicit, adjustable thresholds, serving as the benchmark that more complex machine learning models must beat.

## What is Validated (GrassClover Benchmark Findings)
Evaluated on the public **GrassClover dataset** ($n = 261$ biomass-labelled crops across two camera platforms):
- **Uncalibrated hardware error:** Default thresholds applied across different camera sensors showed large systematic error (MAE 30–32%, with +31% bias on grass and -28% on clover).
- **Calibrated transferability:** Calibrating three thresholds on training images (Nikon D810A) and evaluating on an unseen held-out camera system (Sony ILCE-7, $n = 119$) reduced MAE to **19.4% for grass** and **16.9% for legume**, reducing systematic bias to +7.2% and -4.7% respectively.
- **Known limitations:**
  - An error margin of ~17–19% remains substantial; 2D surface canopy cover does not capture shaded understory clover leaves or vertical canopy layering.
  - Vegetative broadleaf weeds without flowers cannot be reliably distinguished by colour alone ($CCC \approx 0$).
  - Simple colour rules cannot replace learned segmentation, but provide an empirical lower bound.

## What Data We Need from a Partner
To validate the framework against realistic on-farm and plot-trial conditions, we are looking for paired datasets:
1. **Top-down quadrat photographs:** Fixed height (~1 m), pointing straight down, diffuse lighting (overcast/shaded), ideally containing a grey reference card or colour chart.
2. **Same-day reference measurements:**
   - Hand-sorted dry-weight fractions (grass, legume, forb, senescent), and/or
   - Independent visual cover estimates from two observers on the same quadrats.
3. **Sample volume:** Ideally $\ge 30$ quadrats per sward type across several cutting dates or trial sites.

## What We Offer
- Full calibration of the Leyloom pipeline for your camera setup and sward types.
- Statistical analysis of your trial data reporting MAE, RMSE, bias, Lin's CCC, and Bland-Altman limits of agreement against human observers.
- Complete data privacy: all raw data remains your property; public release of joint benchmarks occurs only with your explicit written approval.
- Co-authorship on any resulting open-access methods or dataset publications.

---

## Researcher Outreach Email Template (Draft — Do Not Send Automatically)

**Subject:** Measuring grass-clover sward composition from quadrat photos: quick question on your trial data

Dear Dr. [Researcher Surname],

I have developed Leyloom (https://github.com/Arpanthebaap/leyloom, DOI: 10.5281/zenodo.23357579), an open, offline tool and calibration framework for estimating grass, legume, and forb fractions from top-down quadrat photographs.

On the public GrassClover dataset, calibrating its simple colour rules against a held-out camera system achieved a mean absolute error of 16.9% for clover and 19.4% for grass against dry biomass (cutting uncalibrated error in half, though highlighting that non-flowering broadleaf weeds cannot be resolved by colour alone).

I am currently seeking to benchmark this baseline against multi-species ley trial data with paired botanical separation or dual-observer visual estimates. 

**Quick question:** In your recent ley trials, do you routinely collect top-down quadrat photos alongside your botanical hand-separations or visual scoring, and would you be open to running a test calibration on a small sample of your plots?

Best regards,

**Arpan Ghosh**  
Independent Researcher  
GitHub: https://github.com/Arpanthebaap  
Repository: https://github.com/Arpanthebaap/leyloom  
Live Tool: https://arpanthebaap.github.io/leyloom/
