import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rc('figure', figsize=(10, 5))
mpl.rc('image', cmap='gray')

import numpy as np              # noqa: E402
import pandas as pd             # noqa: E402
from pandas import DataFrame, Series  # noqa: E402

import pims                     # noqa: E402
import trackpy as tp            # noqa: E402
from roipoly import MultiRoi    # noqa: E402


frames = pims.ImageSequence("../test/k255e_pos3_mag_tif_invert/*.tif",
                            as_grey=True)

# print(frames[0])  # first frame

img = frames[0]

fig = plt.figure()
plt.imshow(img, interpolation='nearest', cmap="Greys")
plt.title("Click on the button to add a new ROI")

# Draw multiple ROIs
multiroi_unnamed = MultiRoi()

# Draw all ROIs
plt.imshow(img, interpolation='nearest', cmap="Greys")
roi_names = []
for name, roi in multiroi_unnamed.rois.items():
    roi.display_roi()
    # roi.display_mean(img)
    roi_names.append(name)
plt.legend(roi_names, bbox_to_anchor=(1.2, 1.05))
plt.show()

# Show ROI masks

for name, roi in multiroi_unnamed.rois.items():
    # TODO just multiply mask with image in each iteration?
    print(name)
    print(roi.get_mask(img))
    img = roi.get_mask(img)
    plt.imshow(img, cmap="gray")
plt.title('ROI masks of the ROIs')
plt.show()
