#!python
# -*- coding: utf-8 -*-
# @author: Kun

'''
Author: Kun
Date: 2021-09-30 00:45:40
LastEditTime: 2021-09-30 00:48:54
LastEditors: Kun
Description: 
FilePath: /HomoglyphAttacksDetector/utils/image_utils.py
'''

import numpy as np

from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image


def generate_imgs(strings, font_location, font_size, image_size, text_location):
    font = ImageFont.truetype(font_location, font_size)

    str_imgs = []

    for st in strings:
        # Create a single channel image of floats
        img1 = Image.new('F', image_size)
        dimg = ImageDraw.Draw(img1)
        dimg.text(text_location, st.lower(), font=font)

        img1 = np.expand_dims(img1, axis=0)

        str_imgs.append(img1)

    return np.array(str_imgs, dtype=np.float32)


def generate_img(string, font_location, font_size, image_size, text_location):
    font = ImageFont.truetype(font_location, font_size)

    str_imgs = []

    # Create a single channel image of floats
    img1 = Image.new('F', image_size)
    dimg = ImageDraw.Draw(img1)
    dimg.text(text_location, string.lower(), font=font)

    img1 = np.expand_dims(img1, axis=0)

    str_imgs.append(img1)

    return np.array(str_imgs, dtype=np.float32)
