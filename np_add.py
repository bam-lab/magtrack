import skimage.io as io
import numpy as np
import matplotlib.pyplot as plt

img1 = io.imread('/Users/johanan/prog/test/wt_pos1_crop/NDSequence001.tif')
print('shape', img1.shape)
img2 = io.imread('/Users/johanan/prog/test/wt_pos1_crop/NDSequence003.tif')
print('shape', img2.shape)

all_beads_masked = np.empty(img1.shape)

print("shape", all_beads_masked.shape)

img = []

img.append(img1)
img.append(img2)

for image in img:
    all_beads_masked = np.add(all_beads_masked, image)

print(all_beads_masked)
print("shape:", all_beads_masked.shape)

plt.imshow(img1)
plt.show()
