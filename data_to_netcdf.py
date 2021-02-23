import xarray as xr
import pandas as pd
import config
import glob
import os
import tqdm

#dims = ("monomere", "vars", "supercoiling_state", "simulation", "step")


def df_to_data_array(path):

    df = pd.read_csv(path, sep=" ")
    df = df.iloc[:, :-1] # Drop last column
    df.columns = ["x", "y", "z", "state", "strand_x", "strand_y", "strand_z"]
    df = df.loc[:,["x", "y", "z"]]
    ds = df.to_xarray()  # turn dataframe to dataset
    ds = ds.to_array()  # turn dataset to data array
    ds = ds.rename(index="monomere")

    return ds


def _get_dataset(simulation_directory, simulation_name, supercoil_name):

    dss = []

    step_directories = glob.glob(simulation_directory + "/snapshots/*")
    step_names = []
    for step_directory in tqdm.tqdm(step_directories):

        step_name = os.path.basename(step_directory)
        step_names.append(step_name)
        chain_path = glob.glob(step_directory + "/chain.txt")[-1]
        ds = df_to_data_array(chain_path)
        ds = ds.assign_coords({"supercoiling_sigma": supercoil_name, "simulation": simulation_name})
        ds = ds.expand_dims(["supercoiling_sigma", "simulation"])
        dss.append(ds)

    dss = xr.concat(dss, dim="step")
    dss = dss.assign_coords({"step": step_names})

    return dss


def create_netcdf():

    variables = ["x", "y", "z"]
    supercoil_directories = glob.glob(config.raw_data + "*")

    for supercoil_directory in supercoil_directories:

        supercoil_name = os.path.basename(supercoil_directory)

        if supercoil_name in ["0.02, 0.1, 0.03"]:
            print(f"skipping supercoilname: {supercoil_name}")

        simulation_directories = glob.glob(supercoil_directory + "/sim*")

        for simulation_directory in simulation_directories:

            simulation_name = os.path.basename(simulation_directory)

            print("get_dataset")
            ds = _get_dataset(simulation_directory, simulation_name, supercoil_name)
            print(f"simulation name :{simulation_name}")
            ds.to_netcdf(config.netcdf_data_path + f"data_{simulation_name}.nc")
            print("Done")

############################## Main ##############################
supercoil_name = "0.02"
create_netcdf()
# ds = xr.open_mfdataset(config.netcdf_data_path + f"*{supercoil_name}*.nc", chunks={"simulation": 1, "step": 10})
