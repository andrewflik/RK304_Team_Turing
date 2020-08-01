from devCore import create_CMFD_model
from matplotlib import pyplot as plt
import warnings
import os
from pylab import *
import re
from PIL import Image, ImageChops, ImageEnhance
warnings.filterwarnings("ignore")

busterNetModel = create_CMFD_model( './pretrained_devNet.hd5' )
#from api import USCISI_CMD_API
# IMAGE ANALYSIS

# idhar pe FUNCTION BANA DIYO

def convert_to_ela_image(path, quality):
    filename = path
    #resaved_filename = filename.split('.')[0] + '.resaved.jpg'
    #ELA_filename = filename.split('.')[0] + '.ela.png'
    resaved_filename = 'tempresaved.jpg'
    ELA_filename = 'tempela.png'
    
    im = Image.open(filename).convert('RGB')
    im.save(resaved_filename, 'JPEG', quality = quality)
    resaved_im = Image.open(resaved_filename)
    
    ela_im = ImageChops.difference(im, resaved_im)
    
    extrema = ela_im.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff
    
    ela_im = ImageEnhance.Brightness(ela_im).enhance(scale)
    
    return ela_im

import cv2
import numpy as np
from keras.preprocessing import image
# Imports PIL module  
from PIL import Image 
import tensorflow as tf
print(busterNetModel.summary())
img_width, img_height = 64, 64
imageName = "ash.jpg"
img = image.load_img(imageName)
#img = convert_to_ela_image('', 90)
#orgI = img
img = image.img_to_array(img)
img = np.expand_dims(img, axis = 0)
data = busterNetModel.predict(img)
print(data)
plt.imshow(data.squeeze())
#plt.imshow(orgI)
#path = 
#plt.savefig('')
plt.show()