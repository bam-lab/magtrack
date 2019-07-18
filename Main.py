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

import sys
import os

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rc('image', cmap='gray')

import numpy as np  # noqa: E402
from skimage import morphology  # noqa: E402
import pandas as pd  # noqa: E402
import numbers  # noqa: E402

import pims  # noqa: E402
import trackpy as tp  # noqa: E402

from roipoly import MultiRoi, RoiPoly  # noqa: E402


def euc_distance(dx, dy):
    D = np.sqrt(dx**2 + dy**2)
    return D


# Get data path from CLI argument in quotes
data_path = str(sys.argv[1])

# data_path = '../test/wt_pos1_crop/mag1/*.tif'
microns_per_px = 1 / 2.6696

mag_path = data_path.split('/')[-2]
position_path = data_path.split('/')[-3]
results_path = "Results/" + position_path + "/" + mag_path + "/"
os.makedirs(results_path)  # makes all directories in path recursively
try:
    os.makedirs("Results/cell_csvs")
except Exception:
    print("Results/cell_csvs exists")
print(data_path)
print(position_path)

frames = pims.ImageSequence(data_path, as_grey=True)
seconds_per_frame = 60 / len(frames)
print(frames[-1])

# pick immobile beads outside the cell
plt.imshow(frames[-1])
plt.title("Select ROIs for immobile beads")
immobile_rois = MultiRoi()

plt.imshow(frames[-1])
roi_names = []
for name, roi in immobile_rois.rois.items():
    roi.display_roi()
    roi_names.append("bead" + name)
plt.legend(roi_names, bbox_to_anchor=(1.2, 1.05))
plt.savefig(results_path + 'bead_ROIs.svg')
plt.show()

all_beads_masked = np.empty(frames[-1].shape)
print("shape:", all_beads_masked.shape)

immobile_beads_pos = pd.DataFrame()

for name, roi in immobile_rois.rois.items():
    name = "immobile_bead" + name
    bead_frames_masked = []
    mask = roi.get_mask(frames[-1])  # mask from current bead ROI
    # apply mask to each frame
    print(name)
    for frame in frames:
        frame[~mask] = frame.max()
        bead_frames_masked.append(frame)
    # crop bead ROI into smaller image
    chull = morphology.convex_hull_image(mask)
    [rows, columns] = np.where(chull)
    row1 = min(rows)
    row2 = max(rows)
    col1 = min(columns)
    col2 = max(columns)
    immobile_bead_crop = []
    for frame in bead_frames_masked:
        frame = frame[row1:row2, col1:col2]
        immobile_bead_crop.append(frame)
    immobile_bead_first = tp.locate(
        immobile_bead_crop[-1],
        17,
        minmass=5000,
        max_iterations=20,
        percentile=99.995,
        # topn=1,
        invert=True)
    print(immobile_bead_first.head())
    plt.figure()
    tp.annotate(immobile_bead_first, immobile_bead_crop[-1])
    plt.savefig(results_path + 'beads_found.svg')
    immobile_bead = tp.batch(
        immobile_bead_crop,
        17,
        minmass=5000,
        max_iterations=20,
        percentile=99.995,
        # topn=1,
        invert=True)
    immobile_positions = tp.link(immobile_bead, 5, memory=5)
    print(immobile_positions.head())
    immobile_positions_filtered = tp.filter_stubs(immobile_positions,
                                                  len(immobile_bead_crop))
    # Compare number of particles in unfiltered and filtered data.
    print('Before:', immobile_positions['particle'].nunique())
    print('After:', immobile_positions_filtered['particle'].nunique())
    immobile_positions_filtered.index.names = ['']
    print(immobile_positions_filtered)
    tp.plot_traj(immobile_positions_filtered)
    drift = tp.compute_drift(immobile_positions_filtered)
    # keep only x, y, frame columns
    immobile_positions_filtered = immobile_positions_filtered.drop(columns=[
        'mass', 'size', 'ecc', 'signal', 'raw_mass', 'ep', 'particle'
    ])
    # new columns for delta x and delta y, distance from origin and 3distance
    # TODO: 3distance???
    immobile_positions_filtered["1frame_delta_x"] = np.nan
    immobile_positions_filtered["1frame_delta_y"] = np.nan

    for i in range(len(immobile_positions_filtered.index)):
        if i > 0:
            immobile_positions_filtered.at[
                i, '1frame_delta_x'] = immobile_positions_filtered.at[
                    i, 'x'] - immobile_positions_filtered.at[i - 1, 'x']
            immobile_positions_filtered.at[
                i, '1frame_delta_y'] = immobile_positions_filtered.at[
                    i, 'x'] - immobile_positions_filtered.at[i - 1, 'y']
        else:
            immobile_positions_filtered.at[i, '1frame_delta_x'] = 0
            immobile_positions_filtered.at[i, '1frame_delta_y'] = 0
    print("immobile_positions_filtered")
    print(immobile_positions_filtered.head())
    immobile_positions_filtered = immobile_positions_filtered.drop(
        columns=['x', 'y'])
    immobile_beads_pos = pd.concat(
        [immobile_beads_pos, immobile_positions_filtered],
        axis=1)  # horizontal concatenation of DataFrames

# convert duplicate 1frame_delta_x and 1frame_delta_y into averages
immobile_beads_pos = immobile_beads_pos.groupby(
    by=immobile_beads_pos.columns, axis=1).apply(lambda g: g.mean(
        axis=1) if isinstance(g.iloc[0, 0], numbers.Number) else g.iloc[:, 0])

immobile_beads_pos.rename(columns={'1frame_delta_x': 'avg_1frame_delta_x'},
                          inplace=True)
immobile_beads_pos.rename(columns={'1frame_delta_y': 'avg_1frame_delta_y'},
                          inplace=True)

print(immobile_beads_pos.head())

# print(all_beads_masked.shape)
# print(all_beads_masked)
# plt.imshow(all_beads_masked[-1])
# plt.show()

# Select cell ROIs
fig = plt.figure()
plt.imshow(frames[-1])
plt.title("Select cell boundaries")
cell_rois = MultiRoi()  # This instance stores all ROIs

# Draw all ROIs to confirm
plt.imshow(frames[-1])
roi_names = []
for name, roi in cell_rois.rois.items():
    roi.display_roi()
    roi_names.append("cell" + name)
plt.legend(roi_names, bbox_to_anchor=(1.2, 1.05))
plt.savefig(results_path + 'cell_ROIs.svg')
plt.show()

cells_bead_pos = pd.DataFrame()

# Mask cells
for name, roi in cell_rois.rois.items():
    name = "cell" + name
    cell_frames_masked = []
    mask = roi.get_mask(frames[-1])  # get mask from current roi
    # apply mask to each frame and append to list of masked frames
    print(name)
    for frame in frames:
        frame[~mask] = frame.max()
        cell_frames_masked.append(frame)
    data_dir = '/'.join(data_path.split('/')[0:-1])
    print(data_dir)

    # mask fluorescent channel too
    fluo_img = pims.ImageSequence(data_dir + '/*.tif')
    fluo_masked = []
    for fluo_frame in fluo_img:
        fluo_frame[~mask] = 0
        fluo_masked.append(fluo_frame)

    # crop images
    chull = morphology.convex_hull_image(mask)
    [rows, columns] = np.where(chull)
    row1 = min(rows)
    row2 = max(rows)
    col1 = min(columns)
    col2 = max(columns)
    cell_frames_masked_crop = []
    # brightfield cell crop
    for cell_mask_frame in cell_frames_masked:
        cell_mask_frame = cell_mask_frame[row1:row2, col1:col2]
        cell_frames_masked_crop.append(cell_mask_frame)
    # plt.imshow(cell_frames_masked_crop[-1])
    # plt.show()
    # fluorescent crop
    fluo_masked_crop = []
    for fluo_mask_frame in fluo_masked:
        fluo_mask_frame = fluo_mask_frame[row1:row2, col1:col2]
        fluo_masked_crop.append(fluo_mask_frame)

    # pick 1 bead inside cell
    plt.imshow(cell_frames_masked_crop[-1])  # show image
    plt.title("Select ROI for 1 bead inside the cell")
    cell_bead_roi = RoiPoly(color='b')
    cell_bead_mask = cell_bead_roi.get_mask(cell_frames_masked_crop[-1])
    cell_bead_masked = []
    for cell_mask_frame in cell_frames_masked_crop:
        cell_mask_frame[~cell_bead_mask] = cell_mask_frame.max()
        cell_bead_masked.append(cell_mask_frame)
    # crop cell bead
    chull = morphology.convex_hull_image(cell_bead_mask)
    [rows, columns] = np.where(chull)
    row1 = min(rows)
    row2 = max(rows)
    col1 = min(columns)
    col2 = max(columns)
    cell_bead_crop = []
    for cell_masked_frame in cell_frames_masked_crop:
        cell_masked_frame = cell_masked_frame[row1:row2, col1:col2]
        cell_bead_crop.append(cell_masked_frame)
    cell_bead_first = tp.locate(cell_bead_crop[-1],
                                17,
                                minmass=3000,
                                max_iterations=20,
                                percentile=20,
                                invert=True)
    print(cell_bead_first.head())
    plt.figure()
    tp.annotate(cell_bead_first, cell_bead_crop[-1])
    plt.savefig(results_path + 'cell_bead_found.svg')
    cell_bead = tp.batch(cell_bead_crop,
                         17,
                         minmass=3000,
                         max_iterations=20,
                         percentile=20,
                         invert=True)
    cell_bead_positions = tp.link(cell_bead, 5, memory=5)
    print("cell_bead_positions")
    print(cell_bead_positions.head())
    cell_bead_positions_filtered = tp.filter_stubs(cell_bead_positions,
                                                   len(cell_bead_crop))
    # Compare number of particles in unfiltered and filtered data.
    print('Before:', cell_bead_positions['particle'].nunique())
    print('After:', cell_bead_positions_filtered['particle'].nunique())
    cell_bead_positions_filtered.index.names = ['']
    print(cell_bead_positions_filtered)
    tp.plot_traj(cell_bead_positions_filtered)
    # drift = tp.compute_drift(cell_bead_positions_filtered)
    cell_bead_positions_filtered["1frame_delta_x"] = np.nan
    cell_bead_positions_filtered["1frame_delta_y"] = np.nan

    for i in range(len(cell_bead_positions_filtered.index)):
        if i > 0:
            cell_bead_positions_filtered.at[
                i, '1frame_delta_x'] = cell_bead_positions_filtered.at[
                    i, 'x'] - cell_bead_positions_filtered.at[i - 1, 'x']
            cell_bead_positions_filtered.at[
                i, '1frame_delta_y'] = cell_bead_positions_filtered.at[
                    i, 'y'] - cell_bead_positions_filtered.at[i - 1, 'y']
        else:
            cell_bead_positions_filtered.at[i, '1frame_delta_x'] = 0.0
            cell_bead_positions_filtered.at[i, '1frame_delta_y'] = 0.0
    cell_bead_positions_filtered["cell_name"] = name

    for i in range(len(cell_bead_positions_filtered.index)):
        cell_bead_positions_filtered.at[
            i, '1frame_delta_x'] = cell_bead_positions_filtered.at[
                i, '1frame_delta_x'] - immobile_beads_pos.at[
                    i, 'avg_1frame_delta_x']
        cell_bead_positions_filtered.at[
            i, '1frame_delta_y'] = cell_bead_positions_filtered.at[
                i, '1frame_delta_y'] - immobile_beads_pos.at[
                    i, 'avg_1frame_delta_y']
    cell_bead_positions_filtered = cell_bead_positions_filtered.drop(columns=[
        'mass', 'size', 'ecc', 'signal', 'raw_mass', 'ep', 'particle'
    ])
    # timestamp, distance, speed, and fluorescence columns
    cell_bead_positions_filtered['time (s)'] = np.nan
    cell_bead_positions_filtered['distance from origin (µm)'] = np.nan
    cell_bead_positions_filtered['instantaneous_speed (µm/s)'] = np.nan
    cell_bead_positions_filtered['fluorescence'] = np.nan
    for i in range(len(cell_bead_positions_filtered.index)):
        cell_bead_positions_filtered.at[i, 'time (s)'] = float(
            i * seconds_per_frame)
        cell_bead_positions_filtered.at[
            i, 'distance from origin (µm)'] = euc_distance(
                cell_bead_positions_filtered.at[i, 'x'] -
                cell_bead_positions_filtered.at[0, 'x'],
                cell_bead_positions_filtered.at[i, 'y'] -
                cell_bead_positions_filtered.at[0, 'y']) * microns_per_px
        distance = cell_bead_positions_filtered.at[i,
                                                   'distance from origin (µm)']

        time = cell_bead_positions_filtered.at[i, 'time (s)']
        if i > 0:
            delta_x = cell_bead_positions_filtered.at[i, '1frame_delta_x']
            delta_y = cell_bead_positions_filtered.at[i, '1frame_delta_y']
            distance_from_prev_frame = euc_distance(delta_x, delta_y)
            cell_bead_positions_filtered.at[
                i,
                'instantaneous_speed (µm/s)'] = distance_from_prev_frame / time
        else:
            cell_bead_positions_filtered.at[i,
                                            'instantaneous_speed (µm/s)'] = 0.0
        cell_bead_positions_filtered.at[i, 'fluorescence'] = fluo_masked_crop[
            0].sum()
    print("cell_bead_positions_filtered")
    print(cell_bead_positions_filtered.head())
    cell_bead_positions_filtered.to_csv("./Results/cell_csvs/" +
                                        position_path + '_' + mag_path + '_' +
                                        name + '.csv')
print("Finished!")
