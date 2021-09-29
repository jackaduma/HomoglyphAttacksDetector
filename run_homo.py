#!python
# -*- coding: utf-8 -*-
# @author: Kun

"""
Sample code for siamese neural net for detecting spoofing attacks
"""
from __future__ import with_statement
from sklearn.metrics import roc_curve, auc, roc_auc_score


from text_models import string_sim
import random
import os
import numpy as np
import matplotlib.pyplot as plt
import editdistance
# import cPickle as pickle
import pickle
import codecs
import matplotlib

from utils.image_utils import generate_imgs
from vision_models.siamese_cnn import build_model

# matplotlib.use('Agg') # Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.


# If True, then it runs on a very small dataset (and results won't be that great)
isFast = True  # False

dataset_type = 'process'
#dataset_type = 'domain'

OUTPUT_DIR = 'output'

if not os.path.isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

if dataset_type == 'domain':
    OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'domain_results.pkl')
    INPUT_FILE = os.path.join('homo-data', 'domains_spoof.pkl')
    IMAGE_FILE = os.path.join(OUTPUT_DIR, 'domains_roc_curve.png')
    OUTPUT_NAME = 'Domain Spoofing'
elif dataset_type == 'process':
    OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'process_results.pkl')
    INPUT_FILE = os.path.join('homo-data', 'process_spoof.pkl')
    IMAGE_FILE = os.path.join(OUTPUT_DIR, 'process_roc_curve.png')
    OUTPUT_NAME = 'Process Spoofing'
else:
    raise Exception('Unknown dataset type: %s' % (dataset_type,))


if not os.path.isfile(OUTPUT_FILE):
    font_location = "Arial.ttf"
    font_size = 10
    image_size = (150, 12)
    text_location = (0, 0)
    max_epochs = 50  # 25

    with codecs.open(INPUT_FILE, mode="rb") as f:
        data = pickle.load(f)

    # train: 976122, validate: 51380, test: 256886
    if isFast:
        data['train'] = random.sample(data['train'], 70000)
        data['validate'] = random.sample(data['validate'], 10000)
        data['test'] = random.sample(data['test'], 20000)
        max_epochs = 20  # 10

    # organize data and translate from th to tf image ordering via .transpose( (0,2,3,1) )
    X1_train = generate_imgs([x[0] for x in data['train']], font_location,
                             font_size, image_size, text_location).transpose((0, 2, 3, 1))
    X2_train = generate_imgs([x[1] for x in data['train']], font_location,
                             font_size, image_size, text_location).transpose((0, 2, 3, 1))
    y_train = [x[2] for x in data['train']]

    X1_valid = generate_imgs([x[0] for x in data['validate']], font_location,
                             font_size, image_size, text_location).transpose((0, 2, 3, 1))
    X2_valid = generate_imgs([x[1] for x in data['validate']], font_location,
                             font_size, image_size, text_location).transpose((0, 2, 3, 1))
    y_valid = [x[2] for x in data['validate']]

    X1_test = generate_imgs([x[0] for x in data['test']], font_location,
                            font_size, image_size, text_location).transpose((0, 2, 3, 1))
    X2_test = generate_imgs([x[1] for x in data['test']], font_location,
                            font_size, image_size, text_location).transpose((0, 2, 3, 1))
    y_test = [x[2] for x in data['test']]

    model = build_model((12, 150, 1))

    # First figure out how many epochs we need
    max_auc = 0
    max_idx = 0
    for i in range(max_epochs):
        model.fit([X1_train, X2_train], y_train, batch_size=8, epochs=1)
        scores = [-x[0] for x in model.predict([X1_valid, X2_valid])]

        t_auc = roc_auc_score(y_valid, scores)
        if t_auc > max_auc:
            print('Updated best AUC from %f to %f' % (max_auc, t_auc))
            max_auc = t_auc
            max_idx = i+1

    # Train on the correct number of epochs
    model = build_model((12, 150, 1))
    model.fit([X1_train, X2_train], y_train, batch_size=8, epochs=max_idx)

    # Save the NN
    json_string = model.to_json()
    model.save_weights(os.path.join(
        OUTPUT_DIR, dataset_type + '_cnn.h5'), overwrite=True)
    # 之前是 wb 模式  不对，到底写入什么
    with codecs.open(os.path.join(OUTPUT_DIR, dataset_type + '_cnn.json'), 'w') as f:
        f.write(json_string)

    scores = [-x[0] for x in model.predict([X1_test, X2_test])]
    fpr_siamese, tpr_siamese, threshold_siamese = roc_curve(y_test, scores)
    roc_auc_siamese = auc(fpr_siamese, tpr_siamese)
    print("threshold_siamese: ", threshold_siamese)

    #
    # Run Edit distance
    #
    scores = [(editdistance.eval(x[0].lower(), x[1].lower()),
               len(x[0]), 1.0-x[2]) for x in data['test']]

    y_percent_score = [float(x[0])/x[1] for x in scores]

    y_score, _, y_test = zip(*scores)
    fpr_ed, tpr_ed, threshold_ed = roc_curve(y_test, y_score)
    roc_auc_ed = auc(fpr_ed, tpr_ed)
    print("threshold_ed: ", threshold_ed)

    fpr_ps, tpr_ps, threshold_ps = roc_curve(y_test, y_percent_score)
    roc_auc_ps = auc(fpr_ps, tpr_ps)
    print("threshold_ps: ", threshold_ps)

    #
    # Run editdistance visual similarity
    #
    scores = [(string_sim.howConfusableAre(
        x[0].lower(), x[1].lower()), 1.0-x[2]) for x in data['test']]

    y_score, y_test = zip(*scores)
    fpr_edvs, tpr_edvs, threshold_edvs = roc_curve(
        y_test, [-x for x in y_score])
    roc_auc_edvs = auc(fpr_edvs, tpr_edvs)
    print("threshold_edvs: ", threshold_edvs)

    #
    # Store results
    #
    results = {}
    results['editdistance_vs'] = {
        'fpr': fpr_edvs, 'tpr': tpr_edvs, 'threshold': threshold_edvs,
        'auc': roc_auc_edvs}
    results['editdistance'] = {
        'fpr': fpr_ed, 'tpr': tpr_ed, 'threshold': threshold_ed,
        'auc': roc_auc_ed}
    results['editdistance_percent'] = {
        'fpr': fpr_ps, 'tpr': tpr_ps, 'threshold': threshold_ps,
        'auc': roc_auc_ps}
    results['siamese'] = {
        'fpr': fpr_siamese,
        'tpr': tpr_siamese,
        'threshold': threshold_siamese,
        'auc': roc_auc_siamese}

    with codecs.open(OUTPUT_FILE, 'wb') as f:
        pickle.dump(results, f)


class StrToBytes:
    def __init__(self, fileobj):
        self.fileobj = fileobj

    def read(self, size):
        return self.fileobj.read(size).encode()

    def readline(self, size=-1):
        return self.fileobj.readline(size).encode()


with codecs.open(OUTPUT_FILE, "rb") as f:
    results = pickle.load(f)
    # results = pickle.load(StrToBytes(f))
    print(results)
#
# Make Figures
#
fig = plt.figure()
plt.plot(results['siamese']['fpr'], results['siamese']['tpr'], 'b',
         label='Siamese CNN (AUC=%0.4f)' % results['siamese']['auc'])
plt.plot(results['editdistance_vs']['fpr'], results['editdistance_vs']['tpr'], 'g',
         label='Visual edit distance (AUC=%0.4f)' % results['editdistance_vs']['auc'])
plt.plot(results['editdistance']['fpr'], results['editdistance']['tpr'], 'r',
         label='Edit distance (AUC=%0.4f)' % results['editdistance']['auc'])
plt.plot(results['editdistance_percent']['fpr'], results['editdistance_percent']['tpr'],
         label='Percent edit distance (AUC=%0.4f)' % results['editdistance_percent']['auc'])
plt.plot([0, 1], [0, 1], 'k', lw=3, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('{} - Receiver Operating Characteristic'.format(OUTPUT_NAME))
plt.legend(loc="lower right")
fig.savefig(IMAGE_FILE)
plt.show()
