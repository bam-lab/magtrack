import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

import pims
import trackpy as tp


frames = pims.ImageSequence("../test/mag_tif/*.tif", as_grey=True)
print(frames[0])

plt.imshow(frames[0]);
