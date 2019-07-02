import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

import pims
import trackpy as tp

import sys

# PIMS demo
frames = pims.ImageSequence("../test/k255e_pos3_mag_tif_invert/*.tif",
                            as_grey=True)
frame_zero = frames[0]
print(frames[0])
print(len(frames))
# memory overhead of ImageSequence object is very low:
print(sys.getsizeof(frame_zero), "bytes")  # size of frames in memory, bytes

# plt.imshow(frames[0])
# plt.show()

print(frames[123].frame_no)
print(frames[123].metadata)

# feature location

# 1st arg is for the first frame
# 2nd arg is for object diameter in pixels, must be odd integer
# 3rd arg: TrackPy has an option to invert input imgs
# f = tp.locate(frames[0], 11, invert=False)
# # locate() returns a pandas DataFrame
# print(f.head())  # DataFrame.head() shows the first few rows

# plt.figure()  # new figure
# tp.annotate(f, frames[0])  # this has lots of false positives
# plt.show()

# let's see a histogram of total brightness of blobs
# fig, ax = plt.subplots()
# ax.hist(f['mass'], bins=20)
# # label axes:
# ax.set(xlabel='mass', ylabel='count')
# plt.show()

# now we're filtering by brightness (minmass):
f = tp.locate(frames[63], 11, minmass=49000, max_iterations=20)
plt.figure()
tp.annotate(f, frames[63])
plt.show()

# check for subpixel bias (are decimals evenly distributed)
tp.subpx_bias(f)
plt.show()

# locate features in all frames
# TODO return here
time_cutoff = 419
f = tp.batch(frames[:time_cutoff], 11, minmass=49000, max_iterations=20)
print("f length is:", time_cutoff-2)

# link features into particle trajectories
# define max displacement
max_disp = 5
# define frame memory for feature drop-out
frame_memory = 5

t = tp.link_df(f, max_disp, memory=frame_memory)
print(t.head())

# spurious ephemeral trajectory filtering
# filter features that last for a given number of frames
t1 = tp.filter_stubs(t, time_cutoff)
# Compare the number of particles in the unfiltered and filtered data.
print('Before:', t['particle'].nunique())
print('After:', t1['particle'].nunique())

# filter by appearance (size vs mass)
plt.figure()
tp.mass_size(t1.groupby('particle').mean())
plt.show()

t2 = t1[((t1['mass'] > 0.05) & (t1['size'] < 3.0) &  # fix mass
         (t1['ecc'] < 0.3))]

plt.figure()
tp.annotate(t2[t2['frame'] == 0], frames[0])
plt.show()

plt.figure()
tp.plot_traj(t1)
plt.show()
