"""
Visualize a preprocessed EEG segment (FIF) with injected blink annotations.

Context
-------
This example assumes the original EGI `.mff` recording (~90 min continuous EEG)
has already been:
1. Preprocessed into `.fif` format:
   - Montage applied (e.g., GSN-HydroCel-129)
   - Referenced (e.g., average or VREF)
   - Filtered (high-pass 0.5 Hz, low-pass 30–40 Hz)
   - Resampled to 100 Hz
   - Bipolar EOG channels created
2. Segmented into ~30-min FIF files, aligned with driving video sessions.
3. Annotated with blink events derived from CVAT/EAR labels, injected into the FIF
   as MNE `Annotations`.

Purpose of This Script
----------------------
- Load a single **segment-level `.fif`** file (already preprocessed and annotated).
- Open an interactive MNE browser window to inspect EEG/EOG traces together
  with blink annotations.
- Provide a quick QC step to ensure that blink events appear correctly aligned
  in the data stream.

Parameters
----------
file_path : str
    Path to a segment-level `.fif` file containing EEG and injected blink annotations.
    Example: "S01_20170519_043933/seg_annotated_raw.fif"

What You’ll See
---------------
- Interactive time-series plot (`raw.plot`) with:
  * Channels stacked along the y-axis (EEG + bipolar EOG).
  * Time in seconds along the x-axis.
  * Shaded spans or markers representing injected blink annotations.
- You can scroll, zoom, and click annotations to verify their placement.

Notes
-----
- `show=True`: ensures the plot window is displayed immediately.
- `block=True`: keeps the script open until you close the window.
- Useful as a **visual quality check** before running MATLAB blinker, pyblinker,
  or comparator analyses.

Usage
-----
    $ python plot_segment.py

Example
-------
After running this script, the plot should show EEG traces with shaded
regions marking blink annotations (e.g., around 10–12 seconds), confirming
that ground-truth labels were properly aligned with EEG time.

"""

import mne

# Path to the FIF file
file_path = "seg_annotated_raw.fif"

# Read the FIF file
try:
    raw = mne.io.read_raw_fif(file_path, preload=True)
except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")
    exit()

# Plot the raw data
raw.plot(show=True, block=True)