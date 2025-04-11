'''
Created on Apr 7, 2025

@author: oqb
'''
import cv2
import os
import numpy as np

image_folder = 'd:\Profile\oqb\Desktop\presentations\POF2025\Schaefer\pics'

vids = 'interpolate'

if vids == 'non_interpolate':
    
    for result in ['bfield',
                   'flux_density',
                   'trajectory']:
        
        
        
        image_ref = '{}/{}_gap_6.00_shift_0.00.png'.format(image_folder, result)
        frame = cv2.imread(image_ref)
        height, width, layers = frame.shape
        
        
        for s in ['0.00','-16.00','16.00','32.00','-32.00']:
            video_name = '{}_s{}_gap.avi'.format(result,s)
            video = cv2.VideoWriter(os.path.join(image_folder,'vids',video_name), 0, 0.625, (width,height))
        
            for i in ['6.00','15.26','24.53','33.79','43.05']:
                image = '{}/{}_gap_{}_shift_{}.png'.format(image_folder,result,i, s)
                frame = cv2.imread(image)
                resized_frame = cv2.resize(frame,(width,height))
                #cv2.imwrite('')
                print('{} gives frame size {}, originally {}'.format(i,resized_frame.shape, frame.shape))
                video.write(resized_frame)
    
    cv2.destroyAllWindows()
    video.release()
    
else:
    for result in ['flux_density_distribution',
                   'power_distro']:
        
        
        
        image_ref = '{}/{}_gap_6.00_shift_0.00_interpolated.png'.format(image_folder, result)
        frame = cv2.imread(image_ref)
        height, width, layers = frame.shape
        
        
        for s in ['0.00','-16.00','16.00','32.00','-32.00']:
            video_name = '{}_s{}_gap_interpolated.avi'.format(result,s)
            video = cv2.VideoWriter(os.path.join(image_folder,'vids',video_name), 0, 0.625, (width,height))
        
            for i in ['6.00','15.26','24.53','33.79','43.05']:
                image = '{}/{}_gap_{}_shift_{}_interpolated.png'.format(image_folder,result,i, s)
                frame = cv2.imread(image)
                resized_frame = cv2.resize(frame,(width,height))
                #cv2.imwrite('')
                print('{} gives frame size {}, originally {}'.format(i,resized_frame.shape, frame.shape))
                video.write(resized_frame)
    
    cv2.destroyAllWindows()
    video.release()
    