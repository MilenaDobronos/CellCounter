#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import cv2
import matplotlib.pyplot as plt  

myimage = cv2.imread('pics/NIS_L_Image_2025.tif')
grayed = cv2.cvtColor(myimage, cv2.COLOR_BGR2GRAY)
  
blur = cv2.GaussianBlur(grayed, (11, 11), 0)
canny = cv2.Canny(blur, 30, 150, 3)
dilated = cv2.dilate(canny, (1, 1), iterations=0)
  
(counter, hier) = cv2.findContours(
    dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
rgbed = cv2.cvtColor(myimage, cv2.COLOR_BGR2RGB)
cv2.drawContours(rgbed, counter, -1, (0, 255, 0), 2)

plt.imshow(rgbed)
  
print("cells : ", len(counter))
