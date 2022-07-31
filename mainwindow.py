# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from audio import myspectrogram
import os
import cv2
from model import model

theModel=model()

class myGraphicsScene(QtWidgets.QGraphicsScene):
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def mouseMoveEvent(self,event):
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self,event):
        super().mouseReleaseEvent(event)

class myPixmap(QtWidgets.QGraphicsPixmapItem):
    def __init__(self,widget,mainwindow):
        super().__init__(widget)
        self.__record=False
        self.__mainwindow=mainwindow
    
    def mousePressEvent(self, event):
        if event.buttons () == QtCore.Qt.LeftButton:
            self.__record=True
            theModel.addPos(float(event.pos().x())/theModel.getPictureSize()[1]/0.853,float(event.pos().y())/theModel.getPictureSize()[0]/0.848)
    
    def mouseReleaseEvent(self,event):
        if self.__record==True:
            self.__record=False
            theModel.addPos(float(event.pos().x())/theModel.getPictureSize()[1]/0.853,float(event.pos().y())/theModel.getPictureSize()[0]/0.848)
        theModel.clear()
        self.__mainwindow.setPixmap()


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(812, 351)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 811, 351))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.verticalLayoutWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.sizeSliderFreq = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.sizeSliderFreq.setMinimum(1)
        self.sizeSliderFreq.setMaximum(100)
        self.sizeSliderFreq.setOrientation(QtCore.Qt.Horizontal)
        self.sizeSliderFreq.setObjectName("sizeSliderFreq")
        self.horizontalLayout.addWidget(self.sizeSliderFreq)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.horizontalSlider = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout.addWidget(self.horizontalSlider)
        self.checkBoxIfErase = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBoxIfErase.setObjectName("checkBoxIfErase")
        self.horizontalLayout.addWidget(self.checkBoxIfErase)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 3)
        self.horizontalLayout.setStretch(4, 1)
        self.horizontalLayout.setStretch(5, 3)
        self.horizontalLayout.setStretch(6, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.buttonLoad = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonLoad.setObjectName("buttonLoad")
        self.horizontalLayout_3.addWidget(self.buttonLoad)
        self.buttonPlay = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonPlay.setObjectName("buttonPlay")
        self.horizontalLayout_3.addWidget(self.buttonPlay)
        self.buttonSave = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonSave.setObjectName("buttonSave")
        self.horizontalLayout_3.addWidget(self.buttonSave)
        self.buttonRedo = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.buttonRedo.setObjectName("buttonRedo")
        self.horizontalLayout_3.addWidget(self.buttonRedo)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.buttonSave.setDisabled(True)
        self.buttonPlay.setDisabled(True)
        self.buttonRedo.setDisabled(True)

        self.buttonSave.clicked.connect(self.save)
        self.buttonLoad.clicked.connect(self.load)
        self.buttonRedo.clicked.connect(self.redo)
        self.buttonPlay.clicked.connect(self.play)

        self.sizeSliderFreq.valueChanged.connect(self.rankChange)
        self.horizontalSlider.valueChanged.connect(self.sizeFreqChange)
        self.checkBoxIfErase.stateChanged.connect(self.ifEraseChange)
        self.comboBox.currentIndexChanged.connect(self.windowChange)

        self.fileName = None

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_3.setText(_translate("Dialog", "Window:"))
        self.comboBox.setItemText(0, _translate("Dialog", "Rectangle"))
        self.comboBox.setItemText(1, _translate("Dialog", "Hamming"))
        self.label_2.setText(_translate("Dialog", "Rank(1):"))
        self.label.setText(_translate("Dialog", "FilterSize(1):"))
        self.checkBoxIfErase.setText(_translate("Dialog", "Erase Mode"))
        self.buttonLoad.setText(_translate("Dialog", "Load"))
        self.buttonPlay.setText(_translate("Dialog", "Play"))
        self.buttonSave.setText(_translate("Dialog", "Save"))
        self.buttonRedo.setText(_translate("Dialog", "Redo"))

    def setPixmap(self):
        img=cv2.imread("tmp.png")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        x = img.shape[1]
        y = img.shape[0]
        zoomscale=float(self.graphicsView.height())*18/20/y
        theModel.setPictureSize((int(y*zoomscale),int(x*zoomscale)))
        frame = QtGui.QImage(img, x, y, x*3,QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(frame)
        self.item=myPixmap(pix,self)
        self.item.setScale(zoomscale)
        self.scene=myGraphicsScene()
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)

    def load(self):
        self.fileName, filetype = QtWidgets.QFileDialog.getOpenFileName(None,  "Choose Source Audio",  os.getcwd(),"Wav Files (*.wav)")
        if self.fileName=='':
            return
        theModel.changeAudio(self.fileName,self.comboBox.currentText())
        self.setPixmap()
        self.buttonSave.setEnabled(True)
        self.buttonPlay.setEnabled(True)
        self.buttonRedo.setEnabled(True)

    def play(self):
        theModel.play()


    def save(self):
        fileName_choose, filetype = QtWidgets.QFileDialog.getSaveFileName(None,  "Choose Saving Direction",  os.getcwd(),"Wav Files (*.wav)")
        if fileName_choose=='':
            return
        theModel.save(fileName_choose)
        
    def redo(self):
        if not self.fileName is None:
            theModel.changeAudio(self.fileName,self.comboBox.currentText())
        self.setPixmap()

    
    def sizeFreqChange(self,value):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Dialog", "FilterSize({0}):".format(value)))
        theModel.setSizeFreq(value)

    
    def ifEraseChange(self):
        theModel.setErase(self.checkBoxIfErase.isChecked())
    
    def windowChange(self):
        if not self.fileName is None:
            theModel.changeAudio(self.fileName,self.comboBox.currentText())
        self.setPixmap()
    
    def rankChange(self,value):
        _translate = QtCore.QCoreApplication.translate
        self.label_2.setText(_translate("Dialog", "Rank({0}):".format(value)))
        theModel.setRank(value)