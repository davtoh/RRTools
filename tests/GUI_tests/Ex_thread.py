# https://wiki.python.org/moin/PyQt/Threading,_Signals_and_Slots

from builtins import range
import math
import random
import sys
from PyQt4 import QtCore, QtGui


class Window(QtGui.QWidget):

    def __init__(self, parent = None):

        QtGui.QWidget.__init__(self, parent)

        self.thread = Worker()

        label = QtGui.QLabel(self.tr("Number of stars:"))
        self.spinBox = QtGui.QSpinBox()
        self.spinBox.setMaximum(10000)
        self.spinBox.setValue(100)
        self.startButton = QtGui.QPushButton(self.tr("&Start"))
        self.viewer = QtGui.QLabel()
        #self.viewer.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding) # FIXME need to work with setScaledContents
        #self.viewer.setScaledContents(True) # FIXME it ruins the painting
        #self.viewer.setFixedSize(300, 300)
        from RRtool.RRtoolbox import np2qi
        import cv2
        def loadcv(pth,mode=-1,shape=None):
            im = cv2.imread(pth,mode)
            if shape:
                im = cv2.resize(im,shape)
            return np2qi(im)
        path = r"/mnt/4E443F99443F82AF/Dropbox/PYTHON/RRtoolbox/tests/im1_3.png"
        image = loadcv(path,mode=1,shape=(400,400))
        self.image = image
        self.viewer.setPixmap(QtGui.QPixmap.fromImage(image))


        self.connect(self.thread, QtCore.SIGNAL("finished()"), self.updateUi)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"), self.updateUi)
        self.connect(self.thread, QtCore.SIGNAL("output(QRect, QImage)"), self.addImage)
        self.connect(self.startButton, QtCore.SIGNAL("clicked()"), self.makePicture)

        layout = QtGui.QGridLayout()
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.spinBox, 0, 1)
        layout.addWidget(self.startButton, 0, 2)
        layout.addWidget(self.viewer, 1, 0, 1, 3)
        self.setLayout(layout)

        self.setWindowTitle(self.tr("Simple Threading Example"))

    def makePicture(self):

        self.spinBox.setReadOnly(True)
        self.startButton.setEnabled(False)
        #pixmap = QtGui.QPixmap(self.viewer.size())
        #pixmap.fill(QtCore.Qt.black)
        #self.viewer.setPixmap(pixmap)
        self.thread.render(self.viewer.size(), self.spinBox.value())

    def addImage(self, rect, image):

        pixmap = self.viewer.pixmap()
        painter = QtGui.QPainter()
        painter.begin(pixmap)
        painter.drawImage(rect, image)
        painter.end()
        self.viewer.update(rect)

    def updateUi(self):

        self.spinBox.setReadOnly(False)
        self.startButton.setEnabled(True)

class Worker(QtCore.QThread):

    def __init__(self, parent = None):

        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.size = QtCore.QSize(0, 0)
        self.stars = 0

        self.path = QtGui.QPainterPath()
        angle = 2*math.pi/5
        self.outerRadius = 20
        self.innerRadius = 8
        self.path.moveTo(self.outerRadius, 0)
        for step in range(1, 6):
            self.path.lineTo(
                self.innerRadius * math.cos((step - 0.5) * angle),
                self.innerRadius * math.sin((step - 0.5) * angle)
                )
            self.path.lineTo(
                self.outerRadius * math.cos(step * angle),
                self.outerRadius * math.sin(step * angle)
                )
        self.path.closeSubpath()

    def __del__(self):

        self.exiting = True
        self.wait()

    def render(self, size, stars):

        self.size = size
        self.stars = stars
        self.start()

    def run(self):

        # Note: This is never called directly. It is called by Qt once the
        # thread environment has been set up.

        random.seed()
        n = self.stars
        width = self.size.width()
        height = self.size.height()

        while not self.exiting and n > 0:

            image = QtGui.QImage(self.outerRadius * 2, self.outerRadius * 2,
                           QtGui.QImage.Format_ARGB32)
            image.fill(QtGui.qRgba(0, 0, 0, 0))

            x = random.randrange(0, width)
            y = random.randrange(0, height)
            angle = random.randrange(0, 360)
            red = random.randrange(0, 256)
            green = random.randrange(0, 256)
            blue = random.randrange(0, 256)
            alpha = random.randrange(0, 256)

            painter = QtGui.QPainter()
            painter.begin(image)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QtGui.QColor(red, green, blue, alpha))
            painter.translate(self.outerRadius, self.outerRadius)
            painter.rotate(angle)
            painter.drawPath(self.path)
            painter.end()

            self.emit(QtCore.SIGNAL("output(QRect, QImage)"),
                      QtCore.QRect(x - self.outerRadius, y - self.outerRadius,
                            self.outerRadius * 2, self.outerRadius * 2), image)
            n -= 1

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())