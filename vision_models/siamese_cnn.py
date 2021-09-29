#!python
# -*- coding: utf-8 -*-
# @author: Kun

'''
Author: Kun
Date: 2021-09-30 00:50:10
LastEditTime: 2021-09-30 00:56:56
LastEditors: Kun
Description: 
FilePath: /HomoglyphAttacksDetector/vision_models/siamese_cnn.py
'''

import os
import codecs

from keras.optimizers import RMSprop, Adam
from keras import backend as K
from keras.models import Sequential, Model, model_from_json
from keras.layers.advanced_activations import LeakyReLU
from keras.layers import Dense, Input, Lambda, Flatten, Conv2D, MaxPooling2D

from utils.text_utils import eucl_dist_output_shape, euclidean_distance


def contrastive_loss(y_true, y_pred):
    '''Contrastive loss from Hadsell-et-al.'06
    http://yann.lecun.com/exdb/publis/pdf/hadsell-chopra-lecun-06.pdf
    '''
    margin = 1
    return K.mean(y_true * K.square(y_pred) + (1 - y_true) * K.square(K.maximum(margin - y_pred, 0)), axis=-1, keepdims=False)


def build_model(data_shape):
    model = Sequential()

    model.add(Conv2D(128, (5, 5), input_shape=data_shape))
    model.add(LeakyReLU(alpha=.1))

    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(LeakyReLU(alpha=.1))

    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(32))

    input_a = Input(shape=data_shape)
    input_b = Input(shape=data_shape)

    processed_a = model(input_a)
    processed_b = model(input_b)

    distance = Lambda(euclidean_distance, output_shape=eucl_dist_output_shape)(
        [processed_a, processed_b])

    model = Model(input=[input_a, input_b], output=distance)

    # # train
    rms = RMSprop()
    adam = Adam()
    model.compile(loss=contrastive_loss, optimizer=adam)
    # model.compile(loss=contrastive_loss, optimizer=rms)

    return model


def initialize_encoder(self, OUTPUT_DIR, dataset_type):
    """Initialize encoder for translating images to features."""
    # Set locations of models, weights, and feature parameters
    model_file = os.path.join(OUTPUT_DIR, dataset_type + '_cnn.json')
    weight_file = os.path.join(OUTPUT_DIR, dataset_type + '_cnn.h5')

    # Load model
    with codecs.open(model_file, "r") as f:
        model = model_from_json(f.read())
    model.load_weights(weight_file)

    # Set up encoder to convert images to features
    encoder = self._tm.layers[2]
    input_shape = tuple(model.get_layer(model.layers[0].name).input_shape[1:])
    input_a = Input(shape=input_shape)
    encoder(input_a)

    return encoder
