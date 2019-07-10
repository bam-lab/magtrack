import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rc('figure', figsize=(10, 5))
mpl.rc('image', cmap='gray')

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

import pims
import trackpy as tp

from roipoly import RoiPoly

frames = pims.ImageSequence("../test/k255e_pos3_mag_tif_invert/*.tif", as_grey=True)

print(frames[0]) # first frame

plt.imshow(frames[0])
immobile_bead = RoiPoly(color='b')
plt.imshow(frames[0])
immobile_bead.display_roi()
mask = immobile_bead.get_mask(frames[0])
plt.imshow(mask)
