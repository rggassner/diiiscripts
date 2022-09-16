import numpy as np
import cv2
import os

#Apply a hsv filter to all bmp files in the current
#directory, and save the original and modified, side
#by side in the ouput directory

out_dir='1'

def skel(fname):
    image = cv2.imread(fname)
    origi = image.copy()
    result = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([7,12,50])
    upper = np.array([96,166,135])


    mask = cv2.inRange(image, lower, upper)
    result = cv2.bitwise_and(result, result, mask=mask)
    #cv2.imshow('mask', mask)
    #cv2.imshow('result', result)
    #cv2.imshow('origi', origi)
    er = np.concatenate((origi, result), axis=1)
    #cv2.imshow('er',er)
    #cv2.waitKey()
    cv2.imwrite(out_dir+'/'+fname, er)

for file in os.listdir('.'):
    if file.endswith('.bmp'):
        skel(file)
