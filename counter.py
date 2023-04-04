#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np

def detect_circular_cells(image_path, min_radius=10, max_radius=50, dp=1, min_dist=20, canny_thresh=200, accumulator_thresh=20, draw_circles=True):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp, minDist=min_dist,
                               param1=canny_thresh, param2=accumulator_thresh, minRadius=min_radius, maxRadius=max_radius)

    if draw_circles and circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.rectangle(image, (x - r, y - r), (x + r, y + r), (0, 255, 0), 2)

    if circles is not None:
        return len(circles), image
    else:
        return 0, image


num_circles, output_image = detect_circular_cells('pics/NIS_L_Image_2025.tif')
print('Всего клеток:', num_circles)
cv2.imwrite('stack2.jpg', output_image)
cv2.waitKey(0)

