#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, argparse, shutil, cv2
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import SGDClassifier 
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.datasets import load_digits
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.image as mpimg
import timeit

def display_roi(img, df, index):
    pos_x = df.iloc[index, 1:69] # [0->67] 
    pos_y = df.iloc[index, 69:137]

    for i in range(len(pos_x)):
        img = cv2.circle(img, 
                        (np.round(pos_x[i]).astype('uint64'), np.round(pos_y[i]).astype('uint64')), 
                        radius=2, 
                        color=(255, 255, 255), 
                        thickness=-1)

def display_picture(df, index):
    img = cv2.imread('../Dataset/trainset/'+ df['filename'][index] +'.png') 
    display_roi(img, df, index)
    cv2.imshow(df['filename'][index]+'   label '+str(df['label'][index]), img)
    cv2.waitKey(0)  
    cv2.destroyAllWindows()  

def x_point(value, list_pos_x):
    return np.round(list_pos_x[value]).astype('int')

def y_point(value, list_pos_y):
    return np.round(list_pos_y[value]).astype('int')

def label_name(label):
    label_list = ['neutre', 'colere', 'N.A', 'degout', 'peur', 'joie', 'tristesse', 'surprise']
    return label_list[label]

def left_eyebrow(img, list_pos_x, list_pos_y, label):
    '''
    return cropped left eyebrow
    '''
    # departure point
    x = x_point(17, list_pos_x)
    y = y_point(20, list_pos_y)

    # length and height specification
    length = abs(x_point(27, list_pos_x) - x_point(17, list_pos_x))
    height = max([
        abs(x_point(20, list_pos_x) - x_point(19, list_pos_x)),
        abs(y_point(19, list_pos_y) - y_point(17, list_pos_y))
    ])

    crop_img = img[y:y+height, x:x+length].copy()
    #cv2.imshow("left eyebrow: " + label_name(label), crop_img)
    #cv2.waitKey(0)  
    #cv2.destroyAllWindows()  
    return crop_img

def right_eyebrow(img, list_pos_x, list_pos_y, label):
    '''
    return cropped right eyebrow
    '''
    # departure point
    x = x_point(27, list_pos_x)
    y = y_point(23, list_pos_y)

    # length and height specification
    length = abs(x_point(27, list_pos_x) - x_point(26, list_pos_x))
    height = max([
        abs(x_point(23, list_pos_x) - x_point(22, list_pos_x)),
        abs(y_point(23, list_pos_y) - y_point(26, list_pos_y))
    ])

    crop_img = img[y:y+height, x:x+length].copy()
    #cv2.imshow("right eyebrow: " + label_name(label), crop_img)
    #cv2.waitKey(0)  
    #cv2.destroyAllWindows()  
    return crop_img

def between_eyebrow(img, list_pos_x, list_pos_y, label):
    '''
    return cropped between eyebrow
    '''
    # departure point
    x = x_point(21, list_pos_x)
    y = min([y_point(21, list_pos_y), y_point(22, list_pos_y)])

    # length and height specification
    length = abs(x_point(22, list_pos_x) - x_point(21, list_pos_x))
    height = abs(y_point(29, list_pos_y) - y_point(28, list_pos_y))

    crop_img = img[y:y+height, x:x+length].copy()
    #cv2.imshow("right eyebrow: " + label_name(label), crop_img)
    #cv2.waitKey(0)  
    #cv2.destroyAllWindows()  
    return crop_img

def left_eye(img, list_pos_x, list_pos_y, label):
    '''
    return cropped left eye
    '''
    # departure point
    x = x_point(36, list_pos_x)
    y = y_point(38, list_pos_y)

    # length and height specification
    length = abs(x_point(39, list_pos_x) - x_point(36, list_pos_x))
    height = abs(y_point(40, list_pos_y) - y_point(38, list_pos_y))

    crop_img = img[y:y+height, x:x+length].copy()
    #cv2.imshow("left eye: " + label_name(label), crop_img)
    #cv2.waitKey(0)  
    #cv2.destroyAllWindows()  
    return crop_img

def right_eye(img, list_pos_x, list_pos_y, label):
    '''
    return cropped right eye
    '''
    # departure point
    x = x_point(42, list_pos_x)
    y = y_point(43, list_pos_y)

    # length and height specification
    length = abs(x_point(45, list_pos_x) - x_point(42, list_pos_x))
    height = abs(y_point(47, list_pos_y) - y_point(43, list_pos_y))

    crop_img = img[y:y+height, x:x+length].copy()
    #cv2.imshow("right eye: " + label_name(label), crop_img)
    #cv2.waitKey(0)  
    #cv2.destroyAllWindows()  
    return crop_img

def nose(img, list_pos_x, list_pos_y, label):
    '''
    return cropped nose
    '''
    # departure point
    x = x_point(31, list_pos_x)
    y = y_point(28, list_pos_y)

    # length and height specification
    length = abs(x_point(35, list_pos_x) - x_point(31, list_pos_x))
    height = abs(y_point(28, list_pos_y) - y_point(33, list_pos_y))

    crop_img = img[y:y+height, x:x+length].copy()
    #cv2.imshow("nose: " + label_name(label), crop_img)
    #cv2.waitKey(0)  
    #cv2.destroyAllWindows()  
    return crop_img

def mouth(img, list_pos_x, list_pos_y, label):
    '''
    return cropped mouth
    '''
    # departure point
    x = x_point(41, list_pos_x)
    y = min([
        y_point(48, list_pos_y), 
        y_point(51, list_pos_y), 
        y_point(54, list_pos_y)
    ])

    # length and height specification
    length = abs(x_point(46, list_pos_x) - x_point(41, list_pos_x))
    height = abs(
        max([
            y_point(48, list_pos_y),
            y_point(54, list_pos_y),
            y_point(57, list_pos_y)
        ]) -
        min([
            y_point(48, list_pos_y),
            y_point(51, list_pos_y),
            y_point(54, list_pos_y)
        ])
    )

    crop_img = img[y:y+height, x:x+length].copy()
    cv2.imshow("mouth: " + label_name(label), crop_img)
    cv2.waitKey(0)  
    cv2.destroyAllWindows()  
    return crop_img


def roi_extraction(df, index):
    '''
    extract chosen roi
    1. pour chaque ligne (images) 
    2. on extrait les ROI choisi (features)
    3. on ajoute dans un tableau une ligne pour l'image avec en colonne les images cropped
    4. on ajoute dans un tableau le label de l'image
    [image 0]: f1, f2, ..., fn
    [image 0]: 4 #label
    '''   
    img = cv2.imread('../Dataset/trainset/'+ df['filename'][index] +'.png') 
    list_pos_x = df.iloc[index, 1:69] # [0->67] 
    list_pos_y = df.iloc[index, 69:137]
    label = df.iloc[index, 137]
    
    ROI_1 = left_eyebrow(img, list_pos_x, list_pos_y, label)
    ROI_2 = right_eyebrow(img, list_pos_x, list_pos_y, label)
    ROI_3 = between_eyebrow(img, list_pos_x, list_pos_y, label)
    ROI_4 = left_eye(img, list_pos_x, list_pos_y, label)
    ROI_5 = right_eye(img, list_pos_x, list_pos_y, label)
    ROI_6 = nose(img, list_pos_x, list_pos_y, label)
    ROI_7 = mouth(img, list_pos_x, list_pos_y, label)

def read_data():
    df = pd.read_csv('../Dataset/trainset/trainset.csv', encoding='utf-8')
    #display_picture(df, 5)
    roi_extraction(df, 700)
    
def feature_extraction():
    read_data()

def main():
    feature_extraction()
    sys.exit(0)

if __name__ == "__main__":
    main()