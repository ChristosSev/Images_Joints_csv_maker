import pickle
from glob import glob
import os
import pandas as pd
import csv
from csv import writer
import numpy as np
import argparse
import matplotlib.pyplot as plt
from pathlib import Path


#### Parsing the arguments
parser = argparse.ArgumentParser()

parser.add_argument('--path_to_joints',metavar='path_to_joints',  default='', type=str, help='Path of the joints set')
parser.add_argument('--path_to_images',metavar='path_to_img',  default='', type=str, help='Path of the images set')
parser.add_argument('--csv_name',metavar='csv_name',  default='csv_name', type=str, help='name of the csv ')
parser.add_argument('--threshold',metavar='threshold',   type=float, help='value for threshold ')

args= parser.parse_args()

path_joint = args.path_to_joints
path_img = args.path_to_images
csv_name = args.csv_name
threshold = args.threshold


#Creating list for scans and images#

scans = glob(path_joint + '*pkl')
scans.sort()

images =  glob(path_img + '*jpg')
images_list = []

for i in images:

    output_filename_image = os.path.basename(i).split('.')[0]
    images_list.append(output_filename_image)
    images_list.sort()
    #print(images_list)


output_path = 'csv_outputs' + os.sep
if not os.path.exists(output_path):
    print("It doesnt exist!")
    os.makedirs(output_path)


limit= 1.0

def label_maker(fn):   ### for hearacleia

    if  (fn[0]<= threshold and fn[0]> -threshold) and (fn[1]<= threshold and fn[1]> -threshold) and (fn[2]<= threshold and fn[2]> -threshold) and (fn[3]<= 0.01 and fn[3]> -threshold):
        return 0

    if  (fn[0]<= -threshold ) and (fn[1]<= -threshold) and (fn[2]<= -threshold) and (fn[3]<= -threshold):
        return 0

    if  (fn[0]> threshold+limit ) and (fn[1]> threshold+limit) and (fn[2]> threshold+limit) and (fn[3]> threshold+limit):

        return 1

    else:
        return 2

"""
def label_maker(fn):   #for mocap
    if (fn[0] <= 1.5 and fn[0] > -1.5) and (fn[1] <= 1.5 and fn[1] > -1.5) and (
            fn[2] <= 0.5 and fn[2] > -0.5) and (fn[3] <= 0.5 and fn[3] > -0.5):
        return 0

    if (fn[0] <= -1.5) and (fn[1] <= -1.5) and (fn[2] <= -1.5) and (fn[3] <= -1.5):
        return 0

    else:
        return 1
"""

velocity_array=np.empty([1,4])


csv_final = output_path + csv_name+ '.csv'

with open(csv_final,'w') as final_file:
    for s in scans:
        file_to_read = open(s, "rb")
        loaded_dictionary = pickle.load(file_to_read)
        velocity =loaded_dictionary["velocity"]

        vel_out = label_maker(velocity)

        tmp=np.array(velocity).reshape(1,4)
        velocity_array=np.append(velocity_array, tmp,axis=0)

        output_filename = os.path.basename(s).split('.')[0]
        #output_filename_image = os.path.basename(images).split('.')[0]
        final_file.write(output_filename)
        #final_file.write(images_list[])
        final_file.write('\t' + ',' + str(vel_out) + '\n')
        #final_file.write(str(images_list))


for i in range(0,4):
    plt.figure("Velocity for wheel"+ str(i))
    plt.hist(velocity_array[:,i], bins='auto')  # arguments are passed to np.histogram


#plt.show()


final_file.close()

df = pd.read_csv(csv_final, header = None)
headers = ['joint', 'label', 'image_fn']

### appending the images
df[''] = images_list


df.to_csv(output_path + csv_name+ '_final'+ '.csv', index=False, header=headers)

