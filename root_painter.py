# -*- coding: utf-8 -*-
"""root_painter.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cyJvIY4j8xYHe6tQvwKtiHDwyt7ywEup

# Installing and Running Root Painter

First git clone the package
"""

!git clone https://github.com/Abe404/root_painter.git

"""Create a virtual environment"""

!apt-get install python3-venv
!cd root_painter/trainer && python -m venv env

"""And then activate it."""

!cd root_painter/trainer && source ./env/bin/activate

"""Install dependencies in the virtual environment. (takes over 3 minutes)"""

!cd root_painter/trainer && pip install -r requirements.txt

"""# Now let's tests it out"""

!wget http://openi.nlm.nih.gov/imgs/collections/ChinaSet_AllFiles.zip
  !unzip ChinaSet_AllFiles.zip

!unzip ChinaSet_AllFiles.zip

"""The images are big and more than needed for a quick test. So this resizes the data to speed up the training process and data transfer. It only uses 300 of the images.

***Install another package to satisfy the environment***
"""

!apt-get install libfreeimage-dev

"""***Resize Images***"""

import os
import sys
from multiprocessing import Pool
import random
from PIL import Image
import numpy as np
import tqdm
from skimage.io import imread, imsave
from skimage import img_as_ubyte
from skimage.transform import resize

def resize_file(f):
    out_path = os.path.join(out_dir, os.path.splitext(f)[0] + '.jpg')
    if not os.path.isfile(out_path):
        im = imread(os.path.join(src_dir, f))
        h, w = im.shape[:2]
        # resize so smallest dimension is 600
        if w < h:
            new_w = 600
            ratio = new_w/w
            new_h = round(h * ratio)
        else:
            new_h = 600
            ratio = new_h/h
            new_w = round(w * ratio)
        im = resize(im, (new_h, new_w))
        image = Image.fromarray((im * 255).astype(np.uint8))
        rgb_im = image.convert('RGB')
        imsave(out_path, img_as_ubyte(rgb_im))

src_dir = 'ChinaSet_AllFiles/CXR_png/'
out_dir = 'root_painter_sync/datasets/cxr'

assert os.path.isdir(src_dir)
assert not os.path.isdir(out_dir) and not os.path.isfile(out_dir)
fnames = [a for a in os.listdir(src_dir) if os.path.splitext(a)[1] == '.png']

if not os.path.isdir(out_dir):
    os.makedirs(out_dir)

fnames = random.sample(fnames, k=300)
with Pool(processes=16) as pool:
    for _ in tqdm.tqdm(pool.imap_unordered(resize_file, fnames), total=len(fnames)):
        pass

"""Run root painter. This will first create the sync directory.

***Congratz you installed it***
Now all you have to do is run it, and when it asks you the sync directory point to the directory you resized images into (i.e. your_dir/root_painter_sync/datasets/cxr )
"""

#!cd root_painter/trainer && python main.py --syncdir /your_dir/root_painter_sync/datasets/cxr