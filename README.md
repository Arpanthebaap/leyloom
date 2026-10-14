# Leyloom: colour-based estimation of functional-group composition in grass-legume leys from quadrat photographs, with an open validation framework

**Arpan Ghosh** (independent researcher, Korvanta AI) · Version 0.3.0 · MIT licence
Live tool: https://arpanthebaap.github.io/leyloom/ · Code: https://github.com/Arpanthebaap/leyloom

> **Status.** The software is complete and unit-tested on synthetic data. **No field validation has been run yet, and no accuracy is claimed.** Section 5 is deliberately empty until the benchmark in `benchmark/` has been run on real reference data. This README follows the structure of a short paper so the study can be reviewed, reproduced and extended.

## Abstract
Species-rich and grass-legume leys are central to ruminant forage systems, and their botanical composition governs yield, quality and persistence. Measuring composition by hand-sorting cut samples is slow, and visual cover estimates vary between observers, which limits how many plots, dates and farms a study can cover. Leyloom is an open, offline tool that classifies the pixels of a top-down quadrat photograph into grass, legume, forb, senescent material and bare ground using transparent colour rules, and reports cover, legume share and a functional-group Shannon index. We pair the tool with a validation framework that compares its output with reference composition using mean absolute error, bias, Lin's concordance correlation coefficient and Bland-Altman limits of agreement, calibrates thresholds on training sites only, and reports error on held-out sites. The framework is designed so that a simple, inspectable baseline can be honestly compared with learned segmentation models. Results are pending.

## 1. Introduction
Perennial leys with several grass, legume and forb species can raise productivity, persistence and resilience, but studying them at scale needs composition data from many plots, seasons and farms. Botanical separation is accurate but laborious, and visual estimates depend on the observer. Image-based methods can help, yet the strongest published work relies on deep networks trained on large, specialised image sets, which demand data, compute and expertise that many field groups lack.

We ask a practical question: **how far can a transparent, calibratable colour baseline go, and where does it fail?** A baseline with known failure modes is useful in itself, as a screening tool in the field and as the reference any learned model must beat.

**Research questions**
- RQ1. How well does colour-rule cover agree with reference composition (hand-sorted biomass fractions or expert visual cover) for grass, legume and forb?
- RQ2. How much does per-site calibration of three thresholds improve agreement, and does it transfer to unseen sites?
- RQ3. Under which conditions (illumination, growth stage, flowering, senescence, soil colour) does the baseline fail?
- RQ4. Is the baseline's error comparable to the disagreement between two human observers?

## 2. Related work
The GrassClover dataset provides grass-clover canopy images with biomass-labelled crops, synthetic images with pixel labels, and 31,600 unlabeled images, collected with three acquisition systems at 4 to 8 px/mm and across field and plot trials (Skovsen et al., 2019). The same Aarhus group used convolutional neural networks for species distribution mapping in crop mixtures (Skovsen et al., 2020) and runs the CloverSense and SmartGrass project on clover-grass botanical composition for targeted fertilisation. Leyloom does not compete with that work. It supplies a lightweight, open baseline and an evaluation recipe that can be run against such data, and a route for groups without deep-learning infrastructure.

## 3. Methods
### 3.1 Classifier
Each pixel is converted from RGB to hue (0-360), saturation and value (0-1) and assigned the first matching class:

| Priority | Class | Rule |
|---|---|---|
| 1 | Forb (flowers) | V > 0.82 and S < 0.14; or S > 0.4, V > 0.5 and hue in [270, 345] or <= 12; or S > 0.7, V > 0.75 and hue in [46, 64] |
| 2 | Grass / legume | hue in [65, 170], S >= `min_green`, V > 0.12; grass if hue < `hue_split`, otherwise legume |
| 3 | Senescent | hue in [28, 65], S >= `senescent`, V > 0.3 |
| 4 | Bare | all other pixels |

Defaults: `hue_split` = 98, `min_green` = 0.22, `senescent` = 0.30. Implementations in JavaScript (`index.html`) and Python (`src/leyloom/classify.py`) use identical rules.

### 3.2 Outputs
Percent cover per class; composition (grass, legume, forb as a share of their own sum, comparable with biomass fractions); legume share; Shannon H' = -sum(p ln p) over the three groups (maximum ln 3 = 1.10).

### 3.3 Validation design
- **Reference:** hand-sorted dry-weight fractions or two-observer visual cover, same quadrat, same day as the photograph.
- **Sample:** at least 30 quadrats per sward type across several sites, dates and light conditions.
- **Split:** by **site**, never by photograph. Thresholds are fitted on training sites by grid search (hue split 80-130, minimum greenness 0.12-0.32, senescence 0.20-0.40) minimising mean absolute error, and reported on held-out sites.
- **Metrics:** mean absolute error, RMSE, bias, Lin's concordance correlation coefficient (Lin, 1989) and Bland-Altman limits of agreement (Bland and Altman, 1986), per group.
- **Human benchmark:** the same metrics between two observers on the same quadrats (RQ4).
- **Stratified errors:** by illumination, growth stage, flowering and sward type (RQ3).

### 3.4 Planned datasets
See [docs/DATASETS.md](docs/DATASETS.md). The GrassClover dataset (biomass-labelled image crops) is the first public benchmark; own field data from partner ley trials is the second.

## 4. Implementation
- Browser app (`index.html`): offline, no server or account, photos never leave the device; overlay, sliders, plot log, validation panel, CSV export
- Python package (`src/leyloom`): classifier, metrics and calibration
- Benchmark (`benchmark/run_benchmark.py`): reference CSV plus image folder in, metrics tables out
- Tests (`tests/`): pixel classes, cover sums, Shannon bounds, metric identities, and recovery of shifted hue thresholds by calibration

```bash
pip install -e ".[dev]" && pytest
python benchmark/run_benchmark.py --images data/images --reference data/reference.csv \
    --calibrate --test-sites siteC,siteD --out results/
```

## 5. Results
**Pending.** To be generated by `benchmark/run_benchmark.py` on real reference data. Planned tables: (1) default vs calibrated thresholds on held-out sites per group; (2) error stratified by condition; (3) tool vs two human observers. A synthetic end-to-end run confirms the pipeline mechanics only and says nothing about field accuracy.

## 6. Limitations (known and expected)
- Functional groups, not species; forbs without conspicuous flowers are counted as grass or legume
- Pixel cover of the visible canopy is not biomass; occlusion hides lower layers
- Colour depends on light, white balance, wet leaves and camera; thresholds need calibration per setup
- **Known failure:** mid-brown soil (for example RGB 100, 80, 60) is labelled senescent; a unit test documents this
- Dark-green legumes and shaded grass can overlap in hue

## 7. Reproducibility
All thresholds are explicit parameters; both implementations share one rule table; splits are by site; the benchmark writes `metrics.csv` and the chosen thresholds to `results/run.json`. Example data in `data/` (when added) must be labelled synthetic or real with its source and licence.

## 8. Roadmap
1. Run the GrassClover biomass benchmark and report honestly
2. Collect a small paired dataset on partner ley trials
3. Add a learned pixel or segmentation baseline and compare it with the colour rules
4. Add a reference-card colour correction step
5. Add temporal tracking of persistence per plot

## 9. Ethics, data and AI-use statement
No personal data are processed. Photographs from farms require the landowner's consent. Datasets keep their original licences and citations. *Software and documentation were drafted with AI assistance (Claude, Anthropic) and reviewed, run and edited by the author, who is responsible for the content.* Keep or amend this sentence so that it matches what you actually did; most journals require such a disclosure.

## References
- Skovsen, S., Dyrmann, M., Mortensen, A. K., Laursen, M. S., Gislum, R., Eriksen, J., Farkhani, S., Karstoft, H., Jorgensen, R. N. (2019). The GrassClover Image Dataset for Semantic and Hierarchical Species Understanding in Agriculture. *CVPR Workshops*, 2676-2684. doi:10.1109/CVPRW.2019.00325
- Skovsen, S. K., Laursen, M. S., Kristensen, R. K., Rasmussen, J., Dyrmann, M., Eriksen, J., Gislum, R., Jorgensen, R. N., Karstoft, H. (2020). Robust Species Distribution Mapping of Crop Mixtures Using Color Images and Convolutional Neural Networks. *Sensors*. [add volume and pages from the journal page]
- Lin, L. I.-K. (1989). A concordance correlation coefficient to evaluate reproducibility. *Biometrics*, 45(1), 255-268.
- Bland, J. M., Altman, D. G. (1986). Statistical methods for assessing agreement between two methods of clinical measurement. *The Lancet*, 327(8476), 307-310.

## Citing
See `CITATION.cff`. Cite the version you used.

## Licence
MIT. Datasets and papers cited here keep their own licences.
