# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI design.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from skimage import io, exposure, filters, color, transform, morphology

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(300, 480, 191, 61))
        self.startButton.setObjectName("startButton")
        self.processingTypeLabel = QtWidgets.QLabel(self.centralwidget)
        self.processingTypeLabel.setGeometry(QtCore.QRect(320, 400, 151, 31))
        self.processingTypeLabel.setObjectName("processingTypeLabel")
        self.simpleProcessingRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.simpleProcessingRadioButton.setGeometry(QtCore.QRect(270, 440, 82, 17))
        self.simpleProcessingRadioButton.setObjectName("simpleProcessingRadioButton")
        self.advancedProcessingRadioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.advancedProcessingRadioButton.setGeometry(QtCore.QRect(450, 440, 111, 17))
        self.advancedProcessingRadioButton.setObjectName("advancedProcessingRadioButton")
        self.chooseImageLabel = QtWidgets.QLabel(self.centralwidget)
        self.chooseImageLabel.setGeometry(QtCore.QRect(310, 310, 171, 21))
        self.chooseImageLabel.setObjectName("chooseImageLabel")
        self.chooseImageButton = QtWidgets.QPushButton(self.centralwidget)
        self.chooseImageButton.setGeometry(QtCore.QRect(350, 350, 75, 23))
        self.chooseImageButton.setObjectName("chooseImageButton")
        self.inputImageFrame = QtWidgets.QLabel(self.centralwidget)
        self.inputImageFrame.setGeometry(QtCore.QRect(80, 60, 281, 221))
        self.inputImageFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.inputImageFrame.setText("")
        self.inputImageFrame.setObjectName("inputImageFrame")
        self.outputImageFrame = QtWidgets.QLabel(self.centralwidget)
        self.outputImageFrame.setGeometry(QtCore.QRect(440, 60, 281, 221))
        self.outputImageFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.outputImageFrame.setText("")
        self.outputImageFrame.setObjectName("outputImageFrame")
        self.inputImageLabel = QtWidgets.QLabel(self.centralwidget)
        self.inputImageLabel.setGeometry(QtCore.QRect(170, 30, 111, 20))
        self.inputImageLabel.setObjectName("inputImageLabel")
        self.outputImageLabel = QtWidgets.QLabel(self.centralwidget)
        self.outputImageLabel.setGeometry(QtCore.QRect(540, 30, 81, 20))
        self.outputImageLabel.setObjectName("outputImageLabel")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.chooseImageButton.clicked.connect(self.setImage)
        self.startButton.clicked.connect(self.processImage)
        self.resultPath = None
        self.simpleProcessingRadioButton.setChecked(True)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Retinal Vessel Recognizer"))
        self.startButton.setText(_translate("mainWindow", "Rozpocznij przetwarzanie"))
        self.processingTypeLabel.setText(_translate("mainWindow", "Wybierz sposób przetwarzania"))
        self.simpleProcessingRadioButton.setText(_translate("mainWindow", "Proste"))
        self.advancedProcessingRadioButton.setText(_translate("mainWindow", "Zaawansowane"))
        self.chooseImageLabel.setText(_translate("mainWindow", "Wybierz obraz do przetworzenia"))
        self.chooseImageButton.setText(_translate("mainWindow", "Przeglądaj.."))
        self.inputImageLabel.setText(_translate("mainWindow", "Przetwarzany obraz"))
        self.outputImageLabel.setText(_translate("mainWindow", "Obraz wynikowy"))

    def setImage(self):
        self.imagePath, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Wybierz obraz", "",
                                    "Image Files (*.png *.jpg *.jpeg *.bmp);; Dicom Files (*.dcm)")
        if self.imagePath:
            pixmap = QtGui.QPixmap(self.imagePath)
            pixmap = pixmap.scaled(self.inputImageFrame.width(), self.inputImageFrame.height(), QtCore.Qt.KeepAspectRatio)
            self.inputImageFrame.setPixmap(pixmap)
            self.inputImageFrame.setAlignment(QtCore.Qt.AlignCenter)

    def showResultingImage(self):
        img = QtGui.QImage(self.resultPath)
        pixmap = QtGui.QPixmap(img)
        pixmap = pixmap.scaled(self.outputImageFrame.width(), self.outputImageFrame.height(), QtCore.Qt.KeepAspectRatio)
        self.outputImageFrame.setPixmap(pixmap)
        self.outputImageFrame.setAlignment(QtCore.Qt.AlignLeft)

    def processImage(self):
        if self.simpleProcessingRadioButton.isChecked():
            self.simpleProcessing()
        else:
            self.advancedProcessing()

    def simpleProcessing(self):
        img = io.imread(self.imagePath)
        self.resultPath = self.imagePath
        self.showResultingImage()

    def advancedProcessing(self):
        pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)



if __name__ == "__main__":
    import sys
    sys.excepthook = except_hook
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
