import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rc('image', cmap='gray')

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from pandas import DataFrame, Series  # noqa: E402

import pims  # noqa: E402
import trackpy as tp  # noqa: E402
from roipoly import RoiPoly  # noqa: E402

frames = pims.ImageSequence("../test/wt_pos1/mag1/*.tif",
                            as_grey=True)

# print(frames[0])  # first frame

plt.imshow(frames[0])  # show the image
immobile_bead = RoiPoly(
    color='b')  # draw the ROI on shown image, shows fig by default

plt.imshow(frames[0])  # show image first
immobile_bead.display_roi()  # overlay ROI on shown image
plt.show()  # show the plot

mask = immobile_bead.get_mask(frames[0])  # call mask attribute from ROI object
print(mask)
plt.imshow(mask)
plt.show()

frame_zero = frames[0]

frame_zero[~mask] = 0
plt.imshow(frame_zero)
plt.show()
