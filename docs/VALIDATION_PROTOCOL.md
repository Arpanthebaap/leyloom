# Validation protocol

Goal: find out how well Leyloom's cover estimates agree with a reference method, and where it fails.

## 1. Photo standard
- Frame 0.5 x 0.5 m (or the project's standard), camera pointing straight down at a fixed height (about 1 m)
- Diffuse light (overcast or shaded), no glare; include a grey card or colour chart
- Same camera and settings (fixed white balance if possible); save JPEG or raw
- Record plot, date, time, weather, sward type, growth stage

## 2. Reference measurement
Within minutes of the photo, in the same frame:
- Visual cover estimate by two observers, and/or
- Botanical separation of a cut sample into grass, legume, forb, senescent; dry at 60 C and weigh

## 3. Sample design
- At least 30 quadrats per sward type, spread over sites, dates (regrowths) and light conditions
- Include extremes: pure grass, pure legume, flowering forbs, lodged or senescent canopy
- Split by site, not by photo, into calibration and test sets

## 4. Analysis
For each group (grass, legume, forb, senescent, bare):
- Mean absolute error, root mean square error and bias (percentage points)
- Lin's concordance correlation coefficient and Bland-Altman plot
- Error by light condition, sward type and growth stage
- Compare against inter-observer disagreement: a tool is useful if it is no worse than two humans differ

## 5. Next step: learned model
- Label pixels (for example with SAM-assisted annotation checked by hand)
- Fine-tune a segmentation model on the calibration sites only
- Report the improvement over the rule-based baseline on held-out sites
- Release the dataset and weights under an open licence if partners agree

## 6. Reporting
State the camera, light conditions, sample sizes and every failure case. Report negative results.
