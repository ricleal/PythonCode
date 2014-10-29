import cv2
import numpy as np
from matplotlib import pyplot as plt

"""

From : 
http://opencvpython.blogspot.com/

"""
 
img = cv2.imread('/home/rhf/Pictures/Screenshot from 2014-10-27 10:28:00.png', 0)
ret1, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
ret2, thresh2 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
ret3, thresh3 = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)
ret4, thresh4 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
ret5, thresh5 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV)
 
thresh = ['img', 'thresh1', 'thresh2', 'thresh3', 'thresh4', 'thresh5']

print "Rets:", ret1, ret2, ret3, ret4, ret5 

for i in xrange(6):
    plt.subplot(2, 3, i + 1), plt.imshow(eval(thresh[i]), 'gray')
    plt.title(thresh[i])
 
plt.show()
