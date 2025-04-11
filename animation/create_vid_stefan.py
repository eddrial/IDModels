'''
Created on Apr 7, 2025

@author: oqb
'''
import cv2
import os
import numpy as np

image_folder = 'd:\Profile\oqb\Desktop\presentations\POF2025\Forces'



for result in ['forcevectorsapple_circ',
               'forcevectorsapple_lin',
               'forcevectorscompapple_circ',
               'forcevectorscompapple_lin']:
    
    
    
    image_ref = '{}/forcevectorsapple_circ0.png'.format(image_folder, result)
    frame = cv2.imread(image_ref)
    height, width, layers = frame.shape
    

    video_name = '{}shift.avi'.format(result)
    video = cv2.VideoWriter(os.path.join(image_folder,'vids',video_name), 0, 4, (width,height))

    for i in range(17):
        image = '{}/{}{}.png'.format(image_folder,result,i)
        frame = cv2.imread(image)
#        resized_frame = cv2.resize(frame,(width,height))
        #cv2.imwrite('')
 #       print('{} gives frame size {}, originally {}'.format(i,resized_frame.shape, frame.shape))
        video.write(frame)

cv2.destroyAllWindows()
video.release()

