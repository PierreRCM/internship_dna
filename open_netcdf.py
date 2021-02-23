import xarray as xr
import config
import useful_func as f
import matplotlib.pyplot as plt
import numpy as np
import tqdm
import glob
import os
import pandas as pd

nc_files = glob.glob(config.netcdf_data_path + "/data_0.02_*")
# w_exp = 40

for sim in nc_files:
    rg_list = []
    ds = xr.open_dataarray(sim)
    sim_name = os.path.basename(sim).split("_")[-1].split(".")[0]
    summary_path = config.raw_data + "0.02/" + sim_name + "/snapshots/"

    for step in ds.step:

        step_name = step.values.tolist()
        sum_path = summary_path + step_name + "/summary.txt"
        raw_list_pos = ds.sel(variable=["x", "y", "z"], step=step).values.squeeze().T
        rg = f.compute_Rg(raw_list_pos)
        rg_ivan = f.get_Rg_from_summary(sum_path)
        print(f"My rg = {rg}, Ivan rg = {rg_ivan}, ratio ivanRG/My_rg = {rg_ivan/rg}")


