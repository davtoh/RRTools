# -*- coding: utf-8 -*-
from __future__ import print_function
from builtins import range
from past.builtins import basestring
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import sys
from pyqtgraph.graphicsItems import ROI, ImageItem


class Scroller(QtGui.QWidget):
    def __init__(self, val):
        QtGui.QWidget.__init__(self)
        mygroupbox = QtGui.QGroupBox('this is my groupbox')
        myform = QtGui.QFormLayout()
        labellist = []
        combolist = []
        for i in range(val):
            labellist.append(QtGui.QLabel('mylabel'))
            combolist.append(QtGui.QComboBox())
            myform.addRow(labellist[i],combolist[i])
        mygroupbox.setLayout(myform)
        scroll = QtGui.QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(scroll)

class DragButton(QtGui.QPushButton):
    # http://stackoverflow.com/a/12221360/5288758
    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.__mouseMovePos = globalPos

        super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        super(DragButton, self).mouseReleaseEvent(event)


def getROI(arr, win ='ROI selector', title = "", preview=True, crop = True, form="rect"):
    """

    :param arr: array to crop
    :param win: window title or instance
    :param title: cropping image title
    :param preview: (True) if true it shows the resulting ROI before
            cropping. It could be more lightweight if disabled to False.
    :param crop: (True) if True it returns the cropped image else the
            ROI and ImageItem objects.
    :param form: "rect" for a rectangular, "ellipse" for an elliptical
            and "circle" for a circular selection of ROI.
    :return:
    """
    ## create GUI
    if isinstance(win,basestring):
        W = pg.GraphicsWindow(size=(400,400), border=True)
        W.setWindowTitle(win)
    else:
        W = win

    h,w = arr.shape[:2]
    # make roi handle
    if isinstance(form, ROI.ROI):
        roi = form
    elif form.lower() == "rect":
        roi = pg.RectROI([0, 0], [h,w], pen=(0,9))
        roi.addRotateHandle([1,0], [0.5, 0.5])
    elif form.lower()== "ellipse":
        roi = pg.EllipseROI([0, 0], [30, 20], pen=(3,9))
    elif form.lower() == "circle":
        roi = pg.CircleROI([0, 0], [20, 20], pen=(4,9))
        roi.getArrayRegion()
    else:
        raise Exception("'{}' ROI type is not recognizable".format(form))

    layout = W.addLayout(row=0, col=0)
    layout.addLabel(title, row=0, col=0) # add label to layout
    img1a = pg.ImageItem(arr) # it only supports float
    box1 = layout.addViewBox(row=1, col=0, lockAspect=True)
    box1.addItem(img1a)
    box1.disableAutoRange('xy')
    box1.autoRange()
    box1.addItem(roi)
    if preview:
        box2 = layout.addViewBox(row=2, col=0, lockAspect=True)
        img1b = pg.ImageItem()
        box2.addItem(img1b)
        box2.disableAutoRange('xy')
        box2.autoRange()
        def update(roi):
            img1b.setImage(roi.getArrayRegion(arr, img1a), levels=(0, arr.max()))
            box2.autoRange()
        roi.sigRegionChanged.connect(update)
        update(roi)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

    if crop:
        return roi.getArrayRegion(arr, img1a)

    img1a.W = W # keep reference so that C/C++ wrapped object is not deleted
    return roi, img1a

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    from RRtoolbox.lib.image import loadcv

    app = QtGui.QApplication([]) # make a quick application
    image = loadcv(r"./../../tests/im1_1.jpg",flags=0,shape=(300,500)).astype(np.float32)
    roi,imgla =  getROI(image, preview=True, form="rect", crop=False)
    #myroi = roi.getArrayRegion(image, imgla)
    myroi, coors = roi.getArrayRegion(image, imgla, returnMappedCoords=True)
    #import pdb; pdb.set_trace()
    print(myroi)
    print(coors)
    print(coors.shape)
    getROI(myroi)