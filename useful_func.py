import numpy as np
import vpython as v
import matplotlib.pyplot as plt
import xarray as xr
import tqdm
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
"""Contain typical function to simulate a 3D polymere"""


def _add_monomere(pos, r):

    theta = np.random.uniform(0, 360)
    phi = np.random.uniform(0, 360)
    x = r * np.sin(theta * np.pi / 180) * np.cos(phi * np.pi / 180)
    y = r * np.sin(theta * np.pi / 180) * np.sin(phi * np.pi / 180)
    z = r * np.cos(theta * np.pi / 180)
    new_pos = pos + np.array([x, y, z])

    return new_pos


def display_polymere_in_3D(list_pos, N, radius=0.01):
    """For a list of position display a rod, with vpython"""
    list_rod = []
    sphere = v.sphere(pos=v.vector(0, 0, 0), radius=0.3, opacity=0.8)  # position of first monomere

    for i in range(1, N+1):

        rod = v.cylinder(pos=v.vector(list_pos[i-1][0], list_pos[i-1][1], list_pos[i-1][2]),
                         axis=v.vector(list_pos[i][0], list_pos[i][1], list_pos[i][2]) - v.vector(list_pos[i-1][0],
                                                                                                     list_pos[i-1][1],
                                                                                                     list_pos[i-1][2]),
                         color=v.color.red, radius=radius, opacity=0.8)
        list_rod.append(rod)

    sphere = v.sphere(pos=v.vector(list_pos[-1][0], list_pos[-1][1], list_pos[-1][2]), radius=0.3, opacity=0.8,
                      color=v.color.green)
    return list_rod


def create_polymere(N, l_khun):
    """Input: int number of monomere, int lenght of monomere
       Output: list size=N+1 containing the initial position of each monomere
               list_pos[-1] is the end position of the polymere"""
    old_pos = np.array([0, 0, 0])
    list_pos = [old_pos]

    for i in range(N):

        list_pos.append(_add_monomere(old_pos, l_khun))

        old_pos = list_pos[-1]

    return list_pos


def parB_gaussian(r, sigma):

    return np.exp(-r**2/(2*sigma**2))


def _parB_bind(r, sigma):

    value = np.random.uniform(0, 1) # value to compare to gaussian
    gauss_value = parB_gaussian(r, sigma)  # arbitrary value of sigma

    if value < gauss_value:  # value between 0 and the probability of bounding, simulate the bounding probability
        # print(value)
        # print(gauss_value)
        bound = 1
    else:

        bound = 0

    return bound


def parb_profile(list_monomere_khun, parb_binding_profile, r0, sigma, normalize=False):

    for i, pos in enumerate(list_monomere_khun):

        r = np.linalg.norm(pos) - np.linalg.norm(r0)
        parb_binding_profile[i] += _parB_bind(r, sigma)

    return parb_binding_profile


def compute_Rg(monomeres_positions):
    """Input: 3d-array of position
        output return Rg of the polymere"""

    r_pos = np.linalg.norm(monomeres_positions, axis=1)  # compute norm over each line
    N = len(r_pos)
    r_cm = np.sum(monomeres_positions, axis=0)/N # compute average position of monomere
    r_cm = np.linalg.norm(r_cm)

    return np.sqrt(np.sum(((r_pos - r_cm))**2)/N)


def plot_configuration(list_pos, s=2):
    """Give a list of position, plot the configuration in a 3D scatter plot"""
    np_list_pos = np.array(list_pos) - np.array(list_pos)[0]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter([np_list_pos[:, 0].mean()], [np_list_pos[:, 1].mean()], [np_list_pos[:, 2].mean()], alpha=1, color="r")
    ax.scatter(np_list_pos[0:, 0], np_list_pos[0:, 1], np_list_pos[0:, 2], alpha=1, s=s)
    plt.show()


def binding_profile(nc_files, parb_binding_profile, w_exp):
    """Give netcdf files, compute the binding profiles of all files, respectively to a gaussian parb concentration"""

    for sim in nc_files:
        ds = xr.open_dataarray(sim)
        parb_binding_profile = [0 for i in range(len(ds.monomere))]
        for step in tqdm.tqdm(ds.step):
            raw_list_pos = ds.sel(variable=["x", "y", "z"], step=step).values.squeeze().T
            center = raw_list_pos.mean(axis=0)
            parb_binding_profile = parb_profile(raw_list_pos.tolist(), parb_binding_profile, r0=center, sigma=w_exp)

    return parb_binding_profile


def get_Rg_from_summary(s_path):

    df = pd.read_csv(s_path)
    Rg_file_value = float(df.to_numpy()[7].tolist()[0].split(":")[-1])  # get gyration radius value from sim

    return Rg_file_value



