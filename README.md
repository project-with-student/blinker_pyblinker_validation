# Blink Detection Validation: MATLAB vs Python

This repository hosts the analysis framework for validating the migration of a MATLAB-based blink detection pipeline (“**blinker**”) to a Python implementation (“**pyblinker**”). It provides standardized comparison scripts, metrics, and visualizations to ensure the new Python workflow matches or improves upon the MATLAB baseline, using **EEG FIF data** annotated with ground-truth blinks from CVAT.

---

## 📌 Project Overview

* **Data**: EEG sessions recorded in EGI `.mff` format (\~90 minutes each) have already been:

  * Preprocessed into `.fif` (0.5–30 Hz band-pass, 100 Hz resample, average reference, EOG channels).
  * Segmented into three \~30-minute FIF files aligned to corresponding driving videos.
  * Annotated with blink events from **CVAT** (manual video labeling) and **EAR** signals.

* **Objective**: Compare **MATLAB blinker** and **Python pyblinker** outputs against each other **and against ground truth**, across all segments and subjects.

* **Analysis Scope**:

  1. **Harmonized preprocessing**: ensure MATLAB & Python use the same filters, resampling, and referencing.
  2. **Blink detection parity**: representative channel, blink counts, and per-blink timing.
  3. **Statistical equivalence**: precision, recall, F1, timing offsets, and equivalence testing.
  4. **Segment scalability**: metrics per segment and aggregated across full sessions.
  5. **Epoch-mode experiments (Python only)**:

     * *No-drop epochs*: evaluate blinks on epochized data with all epochs intact.
     * *Random-drop epochs*: repeat with dropped epochs at varying rates to assess robustness.

---

## 📂 Repository Structure

```
.
├── config/                      # Config files (paths, offsets, params)
├── src/                         # All source code lives here
│   ├── matlab_runner/           # MATLAB scripts to run blinker & export CSVs
│   ├── python_runner/           # Python scripts to run pyblinker & export CSVs
│   ├── comparator/              # Matching & metrics computation
│   │   ├── metrics/             # Precision, recall, F1, Δtime, TOST
│   │   └── report/              # Aggregated outputs (tables, CSVs)
│   └── epoch_mode/              # Pyblinker experiments (no-drop, random-drop)
├── README.md                    # Project documentation

```

---

## ⚙️ Workflow

### Step 1: Run Blink Detection

* **MATLAB**: Run `matlab_runner/blinker_segment.m` → produces per-segment summary CSV + blink table.
* **Python**: Run `python_runner/pyblinker_segment.py` → same outputs, harmonized format.

### Step 2: Comparator

* Input:

  * `*_blinks_python.csv`
  * `*_blinks_matlab.csv`
  * `*_blinks_groundtruth.csv`
* Output:

  * Metrics (system vs system, system vs ground truth)
  * Per-segment + aggregated CSVs
  * Plots (distributions, F1, IoU, Δtime)

### Step 3: Epoch Mode (Python only)

* Run `epoch_mode/run_epoch_experiments.py` with config:

  * Epoch length
  * Drop rates (e.g., 5%, 10%, 20%, 40%)
  * Number of replicates per drop rate
* Output:

  * Epoch-level metrics
  * Sensitivity curves (F1 vs drop rate, coverage vs drop rate)

---

## 📊 Metrics & Acceptance Criteria

* **System↔System**

  * Channel match ≥ 95%
  * Blink count match ≥ 95% (else Δ ≤ 1 blink)
  * F1 ≥ 0.95 at ±50 ms, ≥ 0.97 at ±80 ms
  * Median |Δtime| ≤ 20 ms

* **System↔Ground Truth**

  * F1 ≥ 0.92 (±50 ms)
  * IoU ≥ 0.5 for ≥ 80% of blinks

* **Epoch Mode (exploratory)**

  * F1 degradation ≤ 0.02 at ≤10% drop
  * Median |Δtime| shift ≤ 5 ms
  * Stable reproducibility across replicates

---

## 📈 Example Outputs

* **Per-segment metrics table**:

  | Subject | Segment | System1 | System2 | F1 (±50 ms) | Median Δt (ms) | ΔCount |
  | ------- | ------- | ------- | ------- | ----------- | -------------- | ------ |
  | S01     | Seg-1   | Python  | MATLAB  | 0.96        | 18             | 0      |

* **Aggregate plots**:

  * F1 bar charts (system vs system, vs ground truth)
  * Δtime distribution histograms
  * Bland–Altman plots for blink counts

---

## 🚀 Getting Started

1. Clone this repository.
2. Place preprocessed & annotated FIFs under `data/`.
3. Configure paths & parameters in `config/config.yaml`.
4. Run MATLAB and Python detection scripts to generate CSVs.
5. Run comparator to compute metrics and generate reports.
6. (Optional) Run epoch-mode experiments with pyblinker.

---

## 🔬 Future Directions

* Refined **epoch-first pipelines** for real-time EEG blink detection.
* Extending validation to other ocular artifacts (saccades, microsleeps).
* Incorporation of multimodal ground truth (EOG, video, drowsiness scores).

