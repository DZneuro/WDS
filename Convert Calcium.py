#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
from glob import glob
import os

# Define paths and parameters
outpath = r'dir/'  # Specify output directory for the processed CSV files
data_dir = r'F:\\'  # Directory containing the raw data CSV files
frame_rate = 10  # Frame rate (Hz), e.g., 10Hz or 20Hz
drop_initial_frames = 80  # Number of frames to exclude initially (ones not needed for to calculate baseline F or delta F)
baseline_window = 20  # Number of frames to use for calculating baseline (e.g., 2s before stimulus)

# Get list of all CSV files in the specified data directory
filenames = glob(os.path.join(data_dir, '*.csv'))

# Process each file
for f in filenames:
    # Read the data from CSV
    df = pd.read_csv(f)
    
    # Drop the first unnamed column (if needed)
    df = df.drop(df.columns[0], axis=1)

    # Drop the frames not used in the analysis from the data
    df = df.iloc[drop_initial_frames:].reset_index(drop=True)
    
    # Create a time column based on the frame rate
    time_t = np.linspace(0, df.shape[0] * (1 / frame_rate), num=df.shape[0])
    
    # Calculate the baseline F0 using the first 'baseline_window' frames
    baseline_f0 = df.head(baseline_window).mean(axis=0)
    
    # Compute ΔF/F0
    deltaf_f0 = (df - baseline_f0) / baseline_f0
    
    # Insert the time column into the DataFrame
    deltaf_f0.insert(loc=0, column='Time', value=time_t)
    
    # Save the new DataFrame to CSV with the prefix 'dff_'
    new_name = "dff_" + os.path.basename(f)
    deltaf_f0.to_csv(os.path.join(outpath, new_name), index=False)

