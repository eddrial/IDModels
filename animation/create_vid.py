'''
Created on Apr 7, 2025

@author: oqb
'''
import cv2
import os
import numpy as np

image_folder = 'd:\Profile\oqb\Desktop\presentations\POF2025\Animation\gap_apple'
video_name = 'gap_ver_s32.avi'


image_ref = '{}\ivue32_circular_g6_s-16.png'.format(image_folder)
frame = cv2.imread(image_ref)
height, width, layers = frame.shape

video = cv2.VideoWriter(os.path.join(image_folder,video_name), 0, 20    , (width,height))

for i in np.arange(6,46, 0.25):
    print(i)
    image = 'ivue32_linear_g{}_s32.png'.format(i)
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()