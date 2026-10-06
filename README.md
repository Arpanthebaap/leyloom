# Leyloom

Estimate the botanical composition of grass-clover and species-rich leys from top-down quadrat photographs, entirely in the browser.

Leyloom sorts each pixel of a quadrat photo into **grass, legume, forb (flowers), senescent material and bare ground**, shows the result as a colour overlay, and logs legume share and a functional-group diversity index (Shannon H') per plot and date. Results export to CSV for R or Python.

> **Status: research prototype.** The classifier is rule-based (colour thresholds) and has **not yet been validated** on field data. Do not use its numbers for decisions until you have validated it for your own sward types and cameras. See [docs/VALIDATION_PROTOCOL.md](docs/VALIDATION_PROTOCOL.md).

## Why

Resilience and persistence studies of species-rich leys need botanical composition across many plots, dates and farms. Hand-sorting is slow, and visual cover estimates differ between observers. A calibrated photo method could make repeated, comparable measurements cheaper, especially for on-farm work.

## Features
- Runs offline in any modern browser; no server, account or API key
- Photos never leave your device
- Adjustable thresholds (grass/legume hue split, minimum greenness, senescence sensitivity)
- Overlay to check what the classifier decided
- Plot log with date, sward type, legume share and Shannon H'
- Built-in validation panel: enter hand-measured cover and get mean absolute error and bias
- CSV export

## Quick start
Open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

Deploy on GitHub Pages: push this repo, then Settings > Pages > Deploy from branch `main` (root). A workflow in `.github/workflows/pages.yml` is also included.

## How it works
Each pixel is converted from RGB to hue, saturation and brightness (HSV) and assigned a group by rules:
1. Very bright, low-saturation pixels, and strongly saturated pink, purple or yellow pixels, are **forb** (flowers)
2. Green hues above the minimum greenness are **grass** below the hue split and **legume** above it
3. Yellow-brown pixels are **senescent**
4. Everything else is **bare ground**

H' is the Shannon index over grass, legume and forb cover (maximum ln 3 = 1.10).

## Limitations
- Separates functional groups, not species
- Pixel cover of the visible canopy is not biomass; overlapping layers are hidden
- Shadows, wet leaves, glare and white balance change results; use diffuse light and a fixed camera height
- Forbs without conspicuous flowers are counted as grass or legume
- Thresholds depend on the camera and sward

## Roadmap
1. Validate against hand-sorted quadrats (protocol in `docs/`)
2. Build an open labelled quadrat dataset
3. Train a segmentation model (for example a fine-tuned SegFormer or U-Net) and compare it with the rule-based baseline
4. Add species-level classes for common sown species
5. Add season-to-season persistence tracking per plot

## Repository layout
```
index.html                    the whole app (HTML, CSS, JS)
docs/VALIDATION_PROTOCOL.md   how to test the tool properly
CITATION.cff                  how to cite
LICENSE                       MIT
```

## Contributing
Issues and pull requests are welcome, especially labelled photos with reference cover values (with permission to share).

## License
MIT. See [LICENSE](LICENSE).
