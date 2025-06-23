'''
Created on Apr 7, 2025

@author: oqb
'''
import cv2
import os
import numpy as np

image_folder = 'd:\\Profile\\oqb\\Desktop\\presentations\\POF2025\\Schaefer\\final_plots'

fin_plots = {
    'bfields' : 'bfield',
    'flux_densities' : 'fd',
    'flux_density_distributions' : 'fdd',
    'power_distributions' : 'pd',
    'trajectories': 'traj'
    }

for result in fin_plots:
    
    
    
    image_ref = '{}\\{}\\{}_gap_7.00_shift_0.00.png'.format(image_folder, result, fin_plots[result])
    frame = cv2.imread(image_ref)
    height, width, layers = frame.shape
    
    
    for s in ['0.00','-8.00','8.00','-16.00','16.00']:
        video_name = '{}_s{}_gap.avi'.format(result,s)
        video = cv2.VideoWriter(os.path.join(image_folder,'final_vids',video_name), 0, 5, (width,height))
    
        for i in range(7,48):
            image = '{}\\{}\\{}_gap_{}.00_shift_{}.png'.format(image_folder,result,fin_plots[result],i, s)
            frame = cv2.imread(image)
            resized_frame = cv2.resize(frame,(width,height))
            #cv2.imwrite('')
            print('{} gives frame size {}, originally {}'.format(i,resized_frame.shape, frame.shape))
            video.write(resized_frame)

cv2.destroyAllWindows()

video.release()