# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid")
bead_data = pd.read_csv("Results/all_cells.csv")
microns_per_px = 1 / 5.4533  # 2.6696 for 20x

for i in range(2, 10):
    bead_data[str(str(i) + 'frame_instantaneous_speed (µm/s)')] = bead_data[
        str(str(i) + 'frame_instantaneous_speed (µm/s)')] * microns_per_px

sns.relplot(x="distance from origin (µm)",
            y="instantaneous_speed (µm/s)",
            hue="cell_name",
            style="cell_type",
            data=bead_data)

sns.relplot(x="distance from origin (µm)",
            y="2frame_instantaneous_speed (µm/s)",
            hue="cell_name",
            style="cell_type",
            data=bead_data)

sns.relplot(x="distance from origin (µm)",
            y="3frame_instantaneous_speed (µm/s)",
            hue="cell_name",
            style="cell_type",
            data=bead_data)

sns.relplot(x="distance from origin (µm)",
            y="4frame_instantaneous_speed (µm/s)",
            hue="cell_name",
            style="cell_type",
            data=bead_data)

sns.relplot(x="distance from origin (µm)",
            y="5frame_instantaneous_speed (µm/s)",
            hue="cell_name",
            style="cell_type",
            data=bead_data)

sns.relplot(x="distance from origin (µm)",
            y="6frame_instantaneous_speed (µm/s)",
            hue="cell_name",
            style="cell_type",
            data=bead_data)

sns.relplot(x="distance from origin (µm)",
            y="7frame_instantaneous_speed (µm/s)",
            hue="cell_name",
            style="cell_type",
            data=bead_data)

sns.relplot(x="distance from origin (µm)",
            y="8frame_instantaneous_speed (µm/s)",
            hue="cell_name",
            style="cell_type",
            data=bead_data)

sns.relplot(x="distance from origin (µm)",
            y="9frame_instantaneous_speed (µm/s)",
            hue="cell_name",
            style="cell_type",
            data=bead_data)

sns.relplot(x="distance from origin (µm)",
            y="10frame_instantaneous_speed (µm/s)",
            hue="cell_name",
            style="cell_type",
            data=bead_data)

sns.relplot(x="time (s)",
            y="3frame_instantaneous_speed (µm/s)",
            hue="cell_name",
            style="cell_type",
            data=bead_data)

plt.show()
