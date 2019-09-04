# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid")
bead_data = pd.read_csv("Results/all_cells.csv")
bead_data_193 = pd.read_csv("Results/193.csv")
bead_data_c1 = pd.read_csv("Results/c1.csv")
microns_per_px = 1 / 5.4533  # 2.6696 for 20x

for i in range(2, 10):
    bead_data[str(str(i) + 'frame_instantaneous_speed (µm/s)')] = bead_data[
        str(str(i) + 'frame_instantaneous_speed (µm/s)')] * microns_per_px


# All cells

sns.relplot(x="distance from origin (µm)",
            y="10frame_normalized_speed (a.u.)",
            hue="position",
            style="cell_type",
            data=bead_data)

sns.relplot(x="time (s)",
            y="10frame_normalized_speed (a.u.)",
            hue="position",
            style="cell_type",
            data=bead_data)

sns.relplot(x="distance from origin (µm)",
            y="10frame_slope (Hz)",
            hue="position",
            style="cell_type",
            data=bead_data)

# 193

sns.relplot(x="distance from origin (µm)",
            y="10frame_instantaneous_speed (µm/s)",
            hue="position",
            # style="cell_type",
            data=bead_data_193)

sns.relplot(x="time (s)",
            y="10frame_instantaneous_speed (µm/s)",
            hue="position",
            # style="cell_type",
            data=bead_data_193)

sns.relplot(x="distance from origin (µm)",
            y="10frame_slope (Hz)",
            hue="position",
            # style="cell_type",
            data=bead_data_193)

# c1

sns.relplot(x="distance from origin (µm)",
            y="10frame_instantaneous_speed (µm/s)",
            hue="position",
            # style="cell_type",
            data=bead_data_c1)

sns.relplot(x="time (s)",
            y="10frame_instantaneous_speed (µm/s)",
            hue="position",
            style="cell_type",
            data=bead_data_c1)

sns.relplot(x="distance from origin (µm)",
            y="10frame_slope (Hz)",
            hue="position",
            # style="cell_type",
            data=bead_data_c1)

plt.show()
