#!python
# -*- coding: utf-8 -*-
# @author: Kun

'''
Author: Kun
Date: 2021-09-30 00:46:47
LastEditTime: 2021-09-30 00:48:46
LastEditors: Kun
Description: 
FilePath: /HomoglyphAttacksDetector/utils/text_utils.py
'''

import numpy as np

from keras import backend as K


def euclidean_distance(vects):
    x, y = vects
    return K.sqrt(K.sum(K.square(x - y)+np.random.rand()*.0001, axis=1, keepdims=True))


def eucl_dist_output_shape(shapes):
    shape1, shape2 = shapes
    return (shape1[0], 1)
