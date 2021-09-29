#!python
# -*- coding: utf-8 -*-
# @author: Kun

'''
Author: your name
Date: 2021-08-12 09:34:46
LastEditTime: 2021-08-12 11:00:14
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /malicious-process-detect/infer_homo.py
'''

import os
import codecs
import pickle
import random
import pandas as pd
import numpy as np

from sklearn.metrics import auc, roc_curve
from prettytable import PrettyTable

from run_homo import build_model, generate_imgs



def find_optimal_cutoff(target, predicted):
    """ 
    Find the optimal probability cutoff point for a classification model related to event rate
    Parameters
    ----------
    target : Matrix with dependent or target data, where rows are observations
    predicted : Matrix with predicted data, where rows are observations
    Returns
    -------
    list type, with optimal cutoff value
    """

    fpr, tpr, threshold = roc_curve(target, predicted)

    i = np.arange(len(tpr))

    roc = pd.DataFrame({'tf': pd.Series(tpr-(1-fpr), index=i),
                        'threshold': pd.Series(threshold, index=i)})

    # roc_t = roc.ix[(roc.tf-0).abs().argsort()[:1]]
    roc_t = roc.iloc[(roc.tf-0).abs().argsort()[:1]]

    return list(roc_t['threshold'])



dataset_type = "process"

OUTPUT_DIR = 'output'

OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'process_results.pkl')
INPUT_FILE = os.path.join('homo-data', 'process_spoof.pkl')
IMAGE_FILE = os.path.join(OUTPUT_DIR, 'process_roc_curve.png')
OUTPUT_NAME = 'Process Spoofing'


model = build_model((12, 150, 1))

model.load_weights(os.path.join(
    OUTPUT_DIR, dataset_type + '_cnn.h5'))


font_location = "Arial.ttf"
font_size = 10
image_size = (150, 12)
text_location = (0, 0)

with codecs.open(INPUT_FILE, mode="rb") as f:
    data = pickle.load(f)

data['train'] = random.sample(data['train'], 70000)
data['validate'] = random.sample(data['validate'], 10000)
data['test'] = random.sample(data['test'], 20000)


X1_test = generate_imgs([x[0] for x in data['test']], font_location,
                        font_size, image_size, text_location).transpose((0, 2, 3, 1))
X2_test = generate_imgs([x[1] for x in data['test']], font_location,
                        font_size, image_size, text_location).transpose((0, 2, 3, 1))
y_test = [x[2] for x in data['test']]


print("     data_test    " + "#"*100)
# print(data['test'][:100])


# print("     y_test    " + "#"*100)
# print(y_test[:100])


scores = [-x[0] for x in model.predict([X1_test, X2_test])]

# print("     scores    " + "#"*100)
# print(scores[:100])




fpr_siamese, tpr_siamese, threshold_siamese = roc_curve(y_test, scores)
roc_auc_siamese = auc(fpr_siamese, tpr_siamese)

print("#"*120)
print("threshold_siamese: ", threshold_siamese)
print("roc_auc_siamese: ", roc_auc_siamese)

best_threshold = find_optimal_cutoff(y_test, scores)
print("best_threshold: ", best_threshold)


table = PrettyTable(['X1','X2','GT', 'Score', 'Predict'])
for i in range(50):
    x1 = data['test'][i][0]
    x2 = data['test'][i][1]
    y = y_test[i]  # data['test'][i][2]
    s = scores[i]
    p = 1 if s > best_threshold else 0
    # print("{} \t {} \t {} \t {}".format(x1, x2, y, s))
    table.add_row([x1, x2, y, s, str(p)])

print(table)