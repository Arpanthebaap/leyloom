# Datasets

## 1. GrassClover (public, Aarhus University)
Image and biomass dataset of grass-clover mixtures: biomass-labelled image crops, synthetic images with pixel labels, and 31,600 unlabeled images. Page: https://vision.eng.au.dk/grass-clover-dataset
- Cite: Skovsen et al. (2019), doi:10.1109/CVPRW.2019.00325
- **Before use:** read the dataset terms on the page, download it yourself, and do not redistribute it in this repository. Contact the dataset curator (named on the page) for questions or collaboration.
- **Use here:** biomass-labelled crops give reference species composition for RQ1 and RQ2. Convert its labels to `image,grass,legume,forb,site` percent composition and note any weed class handling in your methods.
- **Caveat:** the images are high resolution with a different camera set-up from phone photos; test both.

## 2. Own data (to collect)
Quadrat photographs from ley trials with same-day hand-sorted fractions or two-observer visual estimates, following `docs/PROTOCOL.md`. Obtain written consent and keep site names. Release only with partner approval.

## 3. Reference CSV format
`image,grass,legume,forb,site` where the three values are percent of their sum (they should add to 100) and `site` is used for the train/test split.
