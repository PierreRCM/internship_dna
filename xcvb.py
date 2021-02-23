import os
import config
import glob
import tqdm
files = glob.glob("/home/martin/Desktop/data/4e6_netcdf/0.1/*")
files += glob.glob("/home/martin/Desktop/data/4e6_netcdf/0.02/*")
files += glob.glob("/home/martin/Desktop/data/4e6_netcdf/0.03/*")
# dest = "/home/martin/Desktop/data/4e6_netcdf/"

for file in files:

    os.rename(file, file + ".nc")