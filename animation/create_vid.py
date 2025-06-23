'''
Created on Apr 7, 2025

@author: oqb
'''
import cv2
import os
import numpy as np

image_folder = 'd:\Profile\oqb\Desktop\presentations\POF2025\Animation\gap_plain_apple'
video_name = 'v_gap_plain.avi'


image_ref = '{}\ivue32_circular_g6.0_s16.png'.format(image_folder)
frame = cv2.imread(image_ref)
height, width, layers = frame.shape

video = cv2.VideoWriter(os.path.join(image_folder,video_name), 0, 40    , (width,height))

for i in np.arange(326):
    print(i)
    gap = (i-6)/8+6
    image = 'ivue32_circular_g{}_s16.png'.format(gap)
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()