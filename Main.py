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


import inpututil as inputu
import os
import fnmatch


import cv2
import numpy as np

# crop image with OpenCV
if __name__ == '__main__':
    # Read image
    im = cv2.imread("image.jpg")  # change filename
    # Select ROI
    r = cv2.selectROI(im)
    # Crop image
    imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

    # Display cropped image
    cv2.imshow("Image", imCrop)
    cv2.waitKey(0)


# Takes directory filepath as input, returns list of TIF filenames inside
def tif_list_gen(filepath):
    exp_loc_prompt = str("Enter the full filepath to experiment directory " +
                         "containing TIFs")
    # The prompt returns \0 if empty
    exp_loc = inputu.input_regex(exp_loc_prompt, "[^\0]+",
                                 "Filepath must not be empty!")
    pattern = "*.tif"
    tif_filepaths = []
    for path, subdirs, files in os.walk(exp_loc):
        for name in files:
            if fnmatch(name, pattern):
                tif_filepaths.append(os.path.join(path, name))
    return tif_filepaths
