import pickle
from glob import glob
import os
import pandas as pd
import csv
from csv import writer


path = '/home/christos_sevastopoulos/Desktop/Extracted_Data/heracleia/joints/'
scans = glob(path + '*pkl')
scans.sort()
#print(len(scans))

path_img = '/home/christos_sevastopoulos/Desktop/Extracted_Data/heracleia/img/'
images =  glob(path_img + '*jpg')
images_list = []
for i in images:

    output_filename_image = os.path.basename(i).split('.')[0]
    images_list.append(output_filename_image)
    images_list.sort()
    #print(images_list)

print(len(images_list))
output_path = 'jonnam' + os.sep
if not os.path.exists(output_path):
    print("It exists!")
    os.makedirs(output_path)

def label_maker(fn):
    mean_vel = (fn[2] + fn[3])/2
    if mean_vel >= 1:
        return 1
    else:
        return 0

with open(output_path + 'bia.csv','w') as final_file:
    for s in scans:
        file_to_read = open(s, "rb")
        loaded_dictionary = pickle.load(file_to_read)
        velocity =loaded_dictionary["velocity"]
        mean_velocity = (velocity[2] + velocity[3])/2
        #print(velocity[2], velocity[3])

        vel_out = label_maker(velocity)

        output_filename = os.path.basename(s).split('.')[0]
        #output_filename_image = os.path.basename(images).split('.')[0]
        final_file.write(output_filename)
        #final_file.write(images_list[])
        final_file.write('\t' + ',' + str(vel_out) + '\n')
        #final_file.write(str(images_list))

final_file.close()

df = pd.read_csv('jonnam/bia.csv', header = None)

df[''] = images_list
df.to_csv('bodo.csv', index=False, header = None)

headers = ['joint', 'label', 'image_fn']

df.to_csv("bodo.csv", header=headers, index=False)


dff = pd.read_csv('bodo.csv')

