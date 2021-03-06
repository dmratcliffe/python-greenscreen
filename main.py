import sys
import time
import cv2
import numpy as np
from gsui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QObject, QThread, pyqtSignal)
from gs import GreenThread
import atexit
import configparser

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super (MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
thread = GreenThread()
filename = "greenscreen_settings.ini"
#delay = 0
def main():
    app = QtWidgets.QApplication(sys.argv)
    m = MainWindow()
    m.show()
    thread.finished.connect(app.exit)
    thread.start()
    thread.setWebcam(0)

    try:
        config = configparser.ConfigParser()
        config.read(filename)
        mc = config['main']
        #delay = int(mc['delay'])
        thread.setWebcam(int(mc['webcam']))
        thread.setR(int(mc['r']))
        thread.setG(int(mc['g']))
        thread.setB(int(mc['b']))
        thread.setThreshold(int(mc['threshold']))
        thread.setKernelType(int(mc['kernelType']))
        thread.setKernelSize(int(mc['kernelSize']))
    except:
        print("No config!")

    #m.ui.spinBoxDelay.setValue(delay)
    m.ui.spinBoxCam.setValue(thread.getWebcam())
    m.ui.spinBoxRed.setValue(thread.getR())
    m.ui.spinBoxGreen.setValue(thread.getG())
    m.ui.spinBoxBlue.setValue(thread.getB())
    m.ui.horizontalSliderThresh.setValue(thread.getThreshold())
    m.ui.comboBoxNoise.setCurrentIndex(thread.getKernelType())
    m.ui.horizontalSliderNoiseSize.setValue(thread.getKernelSize())


    m.ui.pushButtonReset.clicked.connect(lambda: reset(m.ui.spinBoxDelay.value()))
    m.ui.checkBoxGreenScreen.clicked.connect(thread.toggleShowWebcam)
    m.ui.spinBoxCam.valueChanged.connect(lambda: thread.setWebcam(m.ui.spinBoxCam.value()))
    m.ui.spinBoxRed.valueChanged.connect(lambda: thread.setR(m.ui.spinBoxRed.value()))
    m.ui.spinBoxGreen.valueChanged.connect(lambda: thread.setG(m.ui.spinBoxGreen.value()))
    m.ui.spinBoxBlue.valueChanged.connect(lambda: thread.setB(m.ui.spinBoxBlue.value()))
    m.ui.horizontalSliderThresh.valueChanged.connect(lambda: thread.setThreshold(m.ui.horizontalSliderThresh.value()))
    m.ui.comboBoxNoise.currentIndexChanged.connect(lambda: thread.setKernelType(m.ui.comboBoxNoise.currentIndex()))
    m.ui.horizontalSliderNoiseSize.valueChanged.connect(lambda: thread.setKernelSize(m.ui.horizontalSliderNoiseSize.value()))
    atexit.register(exit_handler)
    sys.exit (app.exec_())

def exit_handler():
    try:
        config = configparser.ConfigParser()
        config.add_section('main')
        #config.set('main', 'delay', str(delay))
        config.set('main', 'webcam', str(thread.getWebcam()))
        config.set('main', 'r', str(thread.getR()))
        config.set('main', 'g', str(thread.getG()))
        config.set('main', 'b', str(thread.getB()))
        config.set('main', 'threshold', str(thread.getThreshold()))
        config.set('main', 'kernelType', str(thread.getKernelType()))
        config.set('main', 'kernelSize', str(thread.getKernelSize()))

        with open(filename, 'w') as f:
            config.write(f)
    except:
        print("Failed to write config")

    thread.kill()

def reset(d):
    time.sleep(d)
    thread.reset()


if __name__ == '__main__':
    main ()