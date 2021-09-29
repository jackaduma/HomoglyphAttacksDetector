# **Homoglyph Attacks Detector**

Detecting Homoglyph Attacks with CNN model using Computer Vision method

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/jackaduma/HomoglyphAttacksDetector)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/jackaduma?locale.x=zh_XC)

[**中文说明**](./README.zh-CN.md) | [**English**](./README.md)

------

This code is an implementation for paper: [Detecting Homoglyph Attacks with a Siamese
Neural Network](https://arxiv.org/abs/1805.09738), a nice work on **Detecting Homoglyph Attacks **.

- [x] Dataset
  - [x] offical dataset. [process](./homo-data/process_spoof.pkl), [domain](./homo-data/domains_spoof.pkl)
- [x] Usage
  - [x] Training
  - [x] Inference 
- [x] Demo
- [x] Reference

------

## **Detecting Homoglyph Attacks with a Siamese Neural Network**

### [**Paper Page**](https://arxiv.org/abs/1805.09738)


A homoglyph (name spoofing) attack is a common technique used by adversaries to obfuscate file and domain names. This technique creates process or domain names that are visually similar to legitimate and recognized names. For instance, an attacker may create malware with the name svch0st.exe so that in a visual inspection of running processes or a directory listing, the process or file name might be mistaken as the Windows system process svchost.exe. There has been limited published research on detecting homoglyph attacks. Current approaches rely on string comparison algorithms (such as Levenshtein distance) that result in computationally heavy solutions with a high number of false positives. In addition, there is a deficiency in the number of publicly available datasets for reproducible research, with most datasets focused on phishing attacks, in which homoglyphs are not always used. This paper presents a fundamentally different solution to this problem using a Siamese convolutional neural network (CNN). Rather than leveraging similarity based on character swaps and deletions, this technique uses a learned metric on strings rendered as images: a CNN learns features that are optimized to detect visual similarity of the rendered strings. The trained model is used to convert thousands of potentially targeted process or domain names to feature vectors. These feature vectors are indexed using randomized KD-Trees to make similarity searches extremely fast with minimal computational processing. This technique shows a considerable 13% to 45% improvement over baseline techniques in terms of area under the receiver operating characteristic curve (ROC AUC). In addition, we provide both code and data to further future research.


------

**This repository contains:** 

1. [vision model code](./vision_models/siamese_cnn.py) which implemented the paper.
2. [training scripts](./run_homo.py) to train the model.
3. [inference scripts](./infer_homo.py) - to inference.

------

## **Table of Contents**

- [**Homoglyph Attacks Detector**](#homoglyph-attacks-detector)
  - [**Detecting Homoglyph Attacks with a Siamese Neural Network**](#detecting-homoglyph-attacks-with-a-siamese-neural-network)
    - [**Paper Page**](#paper-page)
  - [**Table of Contents**](#table-of-contents)
  - [**Requirement**](#requirement)
  - [**Usage**](#usage)
    - [**train**](#train)
    - [**inference**](#inference)
  - [**Pretrained**](#pretrained)
  - [**Demo**](#demo)
  - [**Reference**](#reference)
  - [Donation](#donation)
  - [**License**](#license)
  
------



## **Requirement** 

```bash
requirements.txt
```
## **Usage**

### **train**

```python
python run_homo.py
```



### **inference** 
```python
python run_infer.py
```

------

## **Pretrained**

a pretrained model in [output](./output) dir:

[process_cnn.h5](./output/process_cnn.h5)

[process_cnn.json](./output/process_cnn.json)


------

## **Demo**

```
demo.ipynb
```

------

## **Reference**
1. **Detecting Homoglyph Attacks with a Siamese Neural Network**. [Paper](https://arxiv.org/abs/1805.09738)
2. offical code project: **homoglyph**.  [Project](https://github.com/endgameinc/homoglyph)


------

## Donation
If this project help you reduce time to develop, you can give me a cup of coffee :) 

AliPay(支付宝)
<div align="center">
	<img src="./misc/ali_pay.png" alt="ali_pay" width="400" />
</div>

WechatPay(微信)
<div align="center">
    <img src="./misc/wechat_pay.png" alt="wechat_pay" width="400" />
</div>

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://paypal.me/jackaduma?locale.x=zh_XC)

------

## **License**

[MIT](LICENSE) © Kun
