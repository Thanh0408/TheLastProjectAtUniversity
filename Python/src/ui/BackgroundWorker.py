
import sys
import threading
import time

sys.path.append('../imgProcessing')

from ImgProClass import *

class worker(threading.Thread):
    def __init__(self, indices, boxes, class_ids, ui):
        threading.Thread.__init__(self)
        self.indices = indices
        self.boxes = boxes
        self.ui = ui
        self.imgProc = ImgProcessing()
        self.class_ids = class_ids

    def run(self):
        print("Starting " + self.name),
        self.start_robot()
        print("Exiting " + self.name)

    def start_robot(self):
        self.imgProc.run(self.indices, self.boxes, self.class_ids, self.ui)

    def kill(self):
        self.killed = True