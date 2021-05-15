
import sys
import threading
import time

sys.path.append('../imgProcessing')

from ImgProClass import *
from PyQt5 import QtGui
from PyQt5.QtGui import *

class ImgProcWorker(threading.Thread):
    def __init__(self, ui):
        threading.Thread.__init__(self)
        self.ui = ui
        self.imgProc = ImgProcessing()

    def run(self):
        image, confidence, class_ids, boxes, indices = self.imgProc.detect_img()
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        qImg = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        self.ui.num_detected.setText(str(np.array(indices).shape[0]))
        self.ui.image_detect.setPixmap(QtGui.QPixmap(qImg))

    def start_robot(self):
        return 0

    def kill(self):
        self.killed = True