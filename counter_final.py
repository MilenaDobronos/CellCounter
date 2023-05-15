#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QToolTip, QMessageBox, QMenu
from PyQt5.QtCore import QCoreApplication
import sys

def detect_circular_cells(image_path, min_radius=10, max_radius=50, dp=1, min_dist=20, canny_thresh=200, accumulator_thresh=20, draw_circles=True):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp, minDist=min_dist,
                               param1=canny_thresh, param2=accumulator_thresh, minRadius=min_radius, maxRadius=max_radius)
    
    alive = 0
    if draw_circles and circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.rectangle(image, (x - r, y - r), (x + r, y + r), (0, 255, 0), 2)
            if sum(image[y][x])>600:
                alive += 1
                

    if circles is not None:
        return len(circles), alive, image
    else:
        return 0, 0, image

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
        num_circles, num_alive, output_image = detect_circular_cells(self.filepath)
        num_aliveper = (num_alive/(num_circles))*100
        dim = (600, 600)
        resized = cv2.resize(output_image, dim)
        cv2.imwrite('stack2.jpg', output_image)
        cv2.imwrite('stack2_resized.jpg', resized)
        
        self.label.setText("Number of cells: " + str(num_circles) + '\nAlive: ' + str(num_alive) + '\nDead: ' + str(num_circles-num_alive) + '\nAlive_per: ' + str(num_aliveper) + '\nDead_per: ' + str(100-num_aliveper))
        self.labelf.setText("File: " + self.filepath)
        
        self.labelp = QtWidgets.QLabel(self)
        self.labelp.move(300, 100)
        rez = QSize(500, 500)
        pixmap = QPixmap('stack2_resized.jpg')
        pixmap = pixmap.scaled(rez)        
        self.labelp.setPixmap(pixmap)        
        
        self.setCentralWidget(self.labelp)
        self.update()

    def initUI(self):        
        self.setGeometry(200, 200, 800, 800)
        self.setWindowTitle("Cell Сounter v 0.1")

        QToolTip.setFont(QFont('Arial', 10))
        self.setToolTip('You can see final result here')
        self.label = QtWidgets.QLabel(self)
        self.label.setToolTip('You can see final result here')
        self.label.setFont(QFont('Arial', 14))        
        self.label.setText("Cell Count: ")
        self.label.setGeometry(600,40,250,50)
        
        QToolTip.setFont(QFont('Arial', 10))
        self.setToolTip('You can see the name of your file here')
        self.labelf = QtWidgets.QLabel(self)
        self.labelf.setToolTip('You can see the name of your file here')
        self.labelf.setFont(QFont('Arial', 14))        
        self.labelf.setText("File: ")
        self.labelf.setGeometry(90, 40,400,50)


        QToolTip.setFont(QFont('Arial', 10))
        self.setToolTip('This is a button to upload image')
        self.bfile = QtWidgets.QPushButton(self)
        self.bfile.setToolTip('This is a button to upload image')
        self.bfile.setGeometry(100, 400, 200, 50)
        self.bfile.setText("Choose image file")
        self.bfile.clicked.connect(self.dialog)

        QToolTip.setFont(QFont('Arial', 10))
        self.setToolTip('Press this button to proceed calculations')
        self.bok = QtWidgets.QPushButton(self)
        self.bok.setToolTip('Press this button to proceed calculations')
        self.bok.setGeometry(500, 50, 50, 30)
        self.bok.setText("OK")
        self.bok.clicked.connect(self.buttonok_clicked)
        
        
        self.labeli = QtWidgets.QLabel(self)
        self.labeli.setFont(QFont('Arial', 14))        
        self.labeli.setText("Instruction: " + '\n1. Choose the image file' + '\n2. Click OK button' + '\n3. Enjoy the result')
        self.labeli.setGeometry(90,150,250,250)
            
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def update(self):
        self.label.adjustSize()

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()

