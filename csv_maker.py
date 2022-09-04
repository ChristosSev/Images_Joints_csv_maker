import pickle
from glob import glob
import os
import pandas as pd
import csv
from csv import writer
import numpy as np

import matplotlib.pyplot as plt

path = '/home/christos_sevastopoulos/Desktop/berdematex/Extracted_Data/heracleia2/joints/'
scans = glob(path + '*pkl')
scans.sort()


path_img = '/home/christos_sevastopoulos/Desktop/berdematex/Extracted_Data/heracleia2/img/'
images =  glob(path_img + '*jpg')
images_list = []

for i in images:

    output_filename_image = os.path.basename(i).split('.')[0]
    images_list.append(output_filename_image)
    images_list.sort()
    #print(images_list)

print(len(images_list))

output_path = 'christos_csv' + os.sep
if not os.path.exists(output_path):
    print("It doesnt exist!")
    os.makedirs(output_path)

def label_maker(fn):

    if  (fn[0]<= 0.01 and fn[0]> -0.01) and (fn[1]<= 0.01 and fn[1]> -0.01) and (fn[2]<= 0.01 and fn[2]> -0.01) and (fn[3]<= 0.01 and fn[3]> -0.01):
        return 0

    if  (fn[0]<= -0.01 ) and (fn[1]<= -0.01) and (fn[2]<= -0.01) and (fn[3]<= -0.01):
        return 0

    else:
        return 1

velocity_array=np.empty([1,4])

with open(output_path + 'heracleia.csv','w') as final_file:
    for s in scans:
        file_to_read = open(s, "rb")
        loaded_dictionary = pickle.load(file_to_read)
        velocity =loaded_dictionary["velocity"]
        #mean_velocity = (velocity[2] + velocity[3])/2
        #print(velocity[2], velocity[3])

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
    plt.figure(i)
    plt.hist(velocity_array[:,i], bins='auto')  # arguments are passed to np.histogram


plt.show()


final_file.close()

df = pd.read_csv('christos_csv/heracleia.csv', header = None)

df[''] = images_list
df.to_csv('final_her.csv', index=False, header = None)

headers = ['joint', 'label', 'image_fn']

df.to_csv("final_her.csv", header=headers, index=False)

dff = pd.read_csv('final_her.csv')
