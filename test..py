import vpython as v
import pandas as pd
import config
import useful_func as f

chain_file = "/home/martin/Desktop/raw_data_DNA/dsig_5e-3_nS_8e6/0.02/simu1/snapshots/step_53200000/chain.txt"
df = pd.read_csv(chain_file, sep=" ")
list_pos = (df.loc[:, ["#x", "y", "z"]].values/100).tolist()
list_pos.append(list_pos[-1])
f.display_polymere_in_3D(list_pos, len(list_pos))

