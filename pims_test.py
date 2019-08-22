# -*- coding: utf-8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np
import pims
from skimage import morphology
from skimage import filters

frames = pims.ImageSequence("../test/wt_pos1_crop/mag1/", as_grey=True)
print(frames)

img = frames[0]

selem = morphology.disk(10)
img_eq = filters.rank.equalize(img, selem=selem)

frames_eq = [filters.rank.equalize(frame, selem) for frame in frames[1:30]]

plt.imshow(frames_eq[20], cmap=plt.cm.gray)
plt.show()
