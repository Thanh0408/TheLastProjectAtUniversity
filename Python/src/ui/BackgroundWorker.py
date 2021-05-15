
import sys
import threading
import time

sys.path.append('../imgProcessing')

from ImgProClass import *

class worker(threading.Thread):
    def __init__(self, threadID, name, ui):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.ui = ui
        self.killed = False
        self.counter=5

    def run(self):
        print("Starting " + self.name),
        self.start_robot()
        print("Exiting " + self.name)

    def start_robot(self):
        return 0

    def kill(self):
        self.killed = True