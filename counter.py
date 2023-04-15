#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import sys



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


# num_circles, output_image = detect_circular_cells('pics/NIS_L_Image_2025.tif')
# print('Всего клеток:', num_circles)
# cv2.imwrite('stack2.jpg', output_image)
# cv2.waitKey(0)



class MyWindow(QMainWindow):
    filepath = ''
    def dialog(self):

        file , check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                   "", "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
        if check:
             self.filepath = file
    
    def __init__(self):
        super(MyWindow,self).__init__()
        self.initUI()

    def buttonok_clicked(self):
        num_circles, output_image = detect_circular_cells(self.filepath)
        dim = (600, 600)
        resized = cv2.resize(output_image, dim)
        cv2.imwrite('stack2.jpg', output_image)
        cv2.imwrite('stack2_resized.jpg', resized)
        
        self.label.setText("Number of cells: " + str(num_circles))
        self.labelf.setText("File: " + self.filepath)
        
        self.labelp = QtWidgets.QLabel(self)
        self.labelp.move(100, 250)
        rez = QSize(600, 600)
        pixmap = QPixmap('stack2_resized.jpg')
        pixmap = pixmap.scaled(rez)        
        self.labelp.setPixmap(pixmap)        
        
        self.setCentralWidget(self.labelp)
        self.update()

    def initUI(self):        
        self.setGeometry(200, 200, 800, 800)
        self.setWindowTitle("Cell counter v 0.1")

        self.label = QtWidgets.QLabel(self)
        self.label.setFont(QFont('Arial', 12))        
        self.label.setText("Number of cells: ")
        self.label.setGeometry(600,40,250,50)
        
        self.labelf = QtWidgets.QLabel(self)
        self.labelf.setFont(QFont('Arial', 8))        
        self.labelf.setText("File: ")
        self.labelf.setGeometry(170, 50,400,50)

        self.bfile = QtWidgets.QPushButton(self)
        self.bfile.setGeometry(50, 50, 100, 30)
        self.bfile.setText("Choose image file")
        self.bfile.clicked.connect(self.dialog)

        self.bok = QtWidgets.QPushButton(self)
        self.bok.setGeometry(500, 50, 50, 30)
        self.bok.setText("OK")
        self.bok.clicked.connect(self.buttonok_clicked)

    def update(self):
        self.label.adjustSize()
        # self.labelf.adjustSize()        
        # self.labelp.adjustSize()


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()






