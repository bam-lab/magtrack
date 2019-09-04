# Copyright 2019 Johanan Idicula
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import numpy as np

import glob


def euc_distance(dx, dy):
    return np.sqrt(dx**2 + dy**2)


cell_csv_list = glob.glob('./Results/cell_csvs/*.csv')
microns_per_px = 1 / 5.4533  # 2.6696 for 20x
max_sample_range = 10  # frame average maximum
# TODO normalize by maximum speed
cells_bead_data = pd.DataFrame()
for cell_csv_filename in cell_csv_list:
    series = cell_csv_filename.split('_')[-1].split(".")[0]
    image_data = pd.read_csv(cell_csv_filename)
    n_frames = len(image_data['frame'])
    seconds_per_frame = 60 / n_frames
    image_data['distance from origin (µm)'] = image_data[
        'distance from origin (µm)'] * 2.6696 / 5.4533  # converting from 20x to 40x
    for i in range(2, max_sample_range + 1):  # sample range loop
        image_data[str(i) + 'frame_delta_x'] = np.nan
        image_data[str(i) + 'frame_delta_y'] = np.nan
        image_data[str(i) + 'frame_instantaneous_speed (µm/s)'] = np.nan
        image_data[str(i) + 'frame_slope (Hz)'] = np.nan
        image_data[str(i) + 'normalized_speed (a.u.)'] = np.nan
        for j in range(n_frames):  # loop for each frame
            if j > 0 and j % i == 0:  # picking every ith frame
                image_data.at[j, str(i) + 'frame_delta_x'] = image_data.at[
                    j, 'x'] - image_data.at[j - i, 'x']
                image_data.at[j, str(i) + 'frame_delta_y'] = image_data.at[
                    j, 'y'] - image_data.at[j - i, 'y']
                image_data.at[
                    j, str(i) +
                    'frame_instantaneous_speed (µm/s)'] = euc_distance(
                        image_data.at[j, str(i) + 'frame_delta_x'],
                        image_data.at[j, str(i) + 'frame_delta_y']) / (
                            image_data.at[j, 'time (s)'] -
                            image_data.at[j - i, 'time (s)'])
                image_data.at[j, str(i) + 'frame_slope (Hz)'] = abs(
                    (image_data.
                     at[j, str(i) + 'frame_instantaneous_speed (µm/s)'] -
                     image_data.
                     at[j -
                        i, str(i) + 'frame_instantaneous_speed (µm/s)']) /
                    (image_data.at[j, 'distance from origin (µm)'] -
                     image_data.at[j - i, 'distance from origin (µm)']))
                image_data.at[
                    j, str(i) + 'frame_normalized_speed (a.u.)'] = image_data.at[
                        j, str(i) +
                        'frame_instantaneous_speed (µm/s)'] / image_data[
                            str(i) + 'frame_instantaneous_speed (µm/s)'].max()
            elif j == 0:  # set first frame to be zero
                image_data.at[j, str(i) + 'frame_delta_x'] = 0.0
                image_data.at[j, str(i) + 'frame_delta_y'] = 0.0
                image_data.at[j,
                              str(i) +
                              'frame_instantaneous_speed (µm/s)'] = 0.0
                image_data.at[j, str(i) + 'frame_slope (Hz)'] = 0.0
            image_data['position'] = image_data['cell_type'].astype(
                'str') + "_" + image_data['cell_name'].astype('str') + series
    cells_bead_data = pd.concat([cells_bead_data, image_data])
# cells_bead_data = cells_bead_data.drop(columns=['Unnamed: 0'])
cells_bead_data.to_csv("./Results/all_cells.csv")
print('Finished!')
