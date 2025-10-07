# Falcon 9 First-Stage Landing — Lab 1 (Data Collection)

**Goal:** Predict if the Falcon 9 first stage will land successfully.  
This repo contains Lab 1 where we collect SpaceX launch data, enrich it via the v4 API,
and build a clean dataset for modeling.

## Contents
- `Lab1_Collecting_Data.ipynb` — requests, wrangling, helper lookups, and EDA
- `dataset_part_1.csv` — cleaned Falcon 9 subset (with imputed `PayloadMass`)
- `.gitignore` — ignore notebook checkpoints

## Notes
- `LandingPad = NaN` means no pad used.
- `Outcome` is `<landing_success> <landing_type>` (e.g., `True ASDS`).
