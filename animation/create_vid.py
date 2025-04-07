'''
Created on Apr 7, 2025

@author: oqb
'''
import cv2
import os

image_folder = 'd:\Profile\oqb\Desktop\presentations\POF2025\Animation\shift_comp_apple'
video_name = 'lin_shift.avi'


image_ref = '{}\ivue32_circular_0.png'.format(image_folder)
frame = cv2.imread(image_ref)
height, width, layers = frame.shape

video = cv2.VideoWriter(os.path.join(image_folder,video_name), 0, 40    , (width,height))

for i in range(0,362):
    print(i)
    image = 'ivue32_linear_{}.png'.format(i)
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()