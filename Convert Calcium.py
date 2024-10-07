import numpy as np
import pandas as pd
from glob import glob

outpath = r'dir/'  # Specify output directory for the raw calcium response CSV files
cd D:\dir\  # change directory to the directory containing raw data
filenames = glob('*.csv') # Get list of all CSV files in the specified data directory
frame_rate = 10  # Frame rate (Hz), 10Hz
drop_initial_frames = 80  # clean up data by dropping frames not used for calculating baseline F0 or delta F
baseline_window = 20  # baseline window (2s) used to calculate F0


# Process each file
for f in filenames:
    df = pd.read_csv(f);
    df = df.drop(df.columns[0], 1);
    df.drop(index=df.index[:Drop_initial_Frames], axis=0, inplace=True)
    time_t = np.linspace(0,df.shape[0]*(1/frame_rate),num = df.shape[0])
    baseline_f0 = df.head(baseline_window).mean(axis=0);
    deltaf_f0 = (df-baseline_f0)/baseline_f0;
    deltaf_f0.insert(loc=0, column='Time', value=time_t);
    new_name = "dff_"+ f
    deltaf_f0.to_csv(outpath + "\\" + new_name, index =False)

