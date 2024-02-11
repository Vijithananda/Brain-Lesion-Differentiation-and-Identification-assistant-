import cv2
import numpy as np
from matplotlib import pyplot as plt

def generateMask(dimension,points):
    mask = np.zeros(dimension, np.uint8)
    ptsArray = []
    # converts points to contour points
    for point in points:
        ptsArray.append([point[0],point[1]])

    ptsArray = np.array(ptsArray)

    # creating mask with contours
    cv2.drawContours(mask, [ptsArray], -1, (255,255,255),-1,cv2.LINE_AA)

    # thresholding to binary
    ret, newMask = cv2.threshold(mask,20,1,cv2.THRESH_BINARY)

    return newMask