from __future__ import print_function, division
import numpy as np
import pandas as pd
from glob import glob
import os
from torchvision import transforms
import pandas as pd
from skimage import io, transform
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import matplotlib as plt
from PIL import Image
import torch
import torchvision.transforms as transforms
import torchvision
from torch.utils.data import DataLoader, Dataset
import cv2


from sklearn.model_selection import train_test_split


#Creating the folders for positive and negative
positive_set= 'positive_set' + os.sep
if not os.path.exists(positive_set):
    print("It doesnt exist!")
    os.makedirs(positive_set)

negative_set= 'negative_set' + os.sep
if not os.path.exists(negative_set):
    print("It doesnt exist!")
    os.makedirs(negative_set)

df = pd.read_csv('bodo.csv')

positive = df[df["label"] == 1]
list_positive = (positive['image_fn']).tolist()

#print(len(list_positive))

negative = df[df["label"] == 0]
list_negative = (negative['image_fn']).tolist()


source_folder = '/home/christos_sevastopoulos/Desktop/Extracted_Data/heracleia/img/'
destination_folder = positive_set


path_img = '/home/christos_sevastopoulos/Desktop/Extracted_Data/heracleia/img/'
images =  glob(path_img + '*jpg')
images_list = []
for i in images:

    output_filename_image = os.path.basename(i).split('.')[0]
    #print(output_filename_image)
    images_list.append(output_filename_image)
    images_list.sort()
    #print(images_list)


images_list = [eval(i) for i in images_list]


source_folder = r"/home/christos_sevastopoulos/Desktop/Extracted_Data/heracleia/img/"
destination_folder_positive = r"/home/christos_sevastopoulos/PycharmProjects/GAN/positive_set/"
destination_folder_negative = r"/home/christos_sevastopoulos/PycharmProjects/GAN/negative_set/"


import shutil

for i in images_list:
    source = source_folder + str(i) + '.jpg'
    destination = destination_folder

    if i in list_positive:
        shutil.move(source,destination_folder_positive)
    elif i in list_negative:
        shutil.move(source,destination_folder_negative)
    else:
        print("Error!")

