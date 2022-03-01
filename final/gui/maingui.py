#! /usr/bin/env python3

import os, sys, subprocess, cv2, time
import numpy as np
from functools import partial
from PyQt5 import QtWidgets, QtGui, QtCore
from gui import Ui_MainWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Video():
    def __init__(self, capture):
        self.capture = capture
        self.currentFrame = np.array([])

    def captureFrame(self):
        ret, readFrame = self.capture.read()
        return readFrame

    def captureNextFrame(self):
        ret, readFrame = self.capture.read()
        if (ret == True):
            self.currentFrame = cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)

    def convertFrame(self):
        try:
            height, width = self.currentFrame.shape[:2]
            img = QImage(self.currentFrame, width, height, QImage.Format_RGB888)
            img = QPixmap.fromImage(img)
            self.previousFrame = self.currentFrame
            return img
        except:
            return None

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.device= cv2.VideoCapture(0)
        self.palette = QPalette()
        self.palette.setColor(self.backgroundRole(), QColor(192,253,123))
        self.setPalette(self.palette)

        self.comboboxs = [
            self.ui.comboBox,
        ]

        self.pushbuttons = [
            self.ui.pushButton,
        ]

        self.labels = [
            self.ui.label,
            self.ui.label2,
            self.ui.label3,
        ]

        self.ui.pushButton.clicked.connect(self.sendbutton_clicked)
        self.video = Video(cv2.VideoCapture(0))
        self.ui._timer = QTimer(self)
        self.ui._timer.timeout.connect(self.play)
        self.ui._timer.start(1)
        self.update()
        self.ret, self.capturedFrame = self.video.capture.read()

    def play(self):
        try:
            self.start = time.time()
            self.video.captureNextFrame()
            self.labels[2].setPixmap(self.video.convertFrame())
            self.labels[2].setScaledContents(True)
            self.end = time.time()
            self.labels[1].setText(str(round(1 / (self.end - self.start), 2)))
        except TypeError:
            print('No Frame')

    def sendbutton_clicked(self):
        pwd = os.path.dirname(__file__)
        cmd = ['command']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=os.path.join(pwd, '..', 'bin'))
        for stdout_line in iter(process.stdout.readline, b''):
            print(stdout_line)

        # store SpeedDirection
        if self.comboboxs[0].currentIndex() == 0:
            sendText = "C:\\Program Files (x86)\\IntelSWTools\\openvino\\bin\\setupvars.bat"
            os.popen(sendText)
        elif self.comboboxs[0].currentIndex() == 1:
            sendText = "conda.bat activate OV37"
            os.popen(sendText)

        # sendcodeStr = ""
        # for i in sendcode:
        #     sendcodeStr += "{0:02x}".format(i)
        # sendText = "cansend " + self.ui.lineEdit.text() + " 300#" + sendcodeStr
        # os.popen(sendText)



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()