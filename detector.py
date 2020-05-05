# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI design.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from skimage import io, exposure, feature, filters, color, transform, morphology, img_as_float, img_as_bool
from scipy import ndimage
import numpy as np
import cv2
import joblib
from PIL import Image, ImageStat


def classify(filename, classifier, pixelPerCell):
    image = np.array(Image.open(filename))
    gamma=1.8# Gamma < 1 ~ Dark ; Gamma > 1 ~ Bright
    image=((image/255)**(1/gamma))
    # print(image)
    classified = np.full((image.shape[0], image.shape[1]), False)
    margin = pixelPerCell - pixelPerCell // 2
    translation = pixelPerCell // 2
    dataGrey = image[:, :, :]
    #dataGrey[:, :, 0] = 0  # PREPROCESSING
    dataGrey[:, :, 2] = 0
    dataGrey = color.rgb2gray(dataGrey)
    dataGrey = exposure.equalize_adapthist(dataGrey)
    dataGrey = exposure.equalize_adapthist(dataGrey, (50, 50))
    dataGrey = exposure.equalize_adapthist(dataGrey, (300, 300))
    dataGrey = exposure.equalize_adapthist(dataGrey, (150, 150))
    dataGrey = np.where((1 - dataGrey) < 100/255, 1, dataGrey + 100/255)
    #dataGrey = filters.gaussian(dataGrey, sigma=2)
    # print(dataIm.shape, maskIm.shape)\n",
    for i in range(margin, image.shape[0] - margin - 1):
        for j in range(margin, image.shape[1] - margin - 1):
            if (((i - 477) ** 2) + ((j - 494) ** 2)) ** 0.5 > 450:
                classified[i][j] = False
            else:
                subData = []  # tablica na parametry obliczone dla komórki
                # ***skopiowanie fragmentu obrazu
                #print(i, j, i-translation, i+translation+1, j-translation, j+translation+1)
                subImage = image[i - translation:i + translation + 1, j - translation:j + translation + 1, :]
                # print(subImage)
                # ***obliczanie wariancji kolorów:
                varianceR = ndimage.measurements.variance(subImage[:, :, 0])
                varianceG = ndimage.measurements.variance(subImage[:, :, 1])
                subData.append(varianceR)
                subData.append(varianceG)
                #varianceB = ndimage.measurements.variance(subImage[:, :, 2])
                #subData.extend((varianceR, varianceG, varianceB))
                #subData.append(np.mean(subImage))
                #stat = ImageStat.Stat(Image.fromarray(subImage).convert('L'))
                #subData.append(stat.mean[0])
                # ***zamiana na skalę szarości
                # subImage = color.rgb2gray(subImage)
                subImage = dataGrey[i - translation:i + translation + 1, j - translation:j + translation + 1]
                # ***obliczanie momentów Hu
                moments = cv2.moments(subImage)
                huMoments = cv2.HuMoments(moments)
                # print(moments)
                # print(huMoments)
                #cy, cx = ndimage.center_of_mass(subImage)
                #subData.extend((cy, cx))
                #for m in huMoments:
                #    subData.append(m[0])
                subData.extend((huMoments[0][0], huMoments[3][0], huMoments[6][0]))
                    # print(subData)
                # ***predykcja
                # if classifier.predict([subData]):
                # print(i, j)
                classified[i][j] = classifier.predict([subData])
    print(np.count_nonzero(image))
    print(np.count_nonzero(classified))
    return classified


class Ui_mainWindow(object):
    def __init__(self):
        self.IMAGE_WIDTH = 999
        self.IMAGE_HEIGHT = 960
        self.NUM_OF_PIXELS = self.IMAGE_HEIGHT * self.IMAGE_WIDTH

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
        self.outputImageFrame.setAlignment(QtCore.Qt.AlignCenter)

    def processImage(self):
        if self.simpleProcessingRadioButton.isChecked():
            self.simpleProcessing()
        else:
            self.advancedProcessing()

    def simpleProcessing(self):
        newImg = io.imread(self.imagePath)

        newImg[:,:,0] = 0 # PREPROCESSING
        newImg[:,:,2] = 0
        newImg = color.rgb2gray(newImg)
        newImg = exposure.equalize_adapthist(newImg)
        newImg = exposure.equalize_adapthist(newImg, (50, 50))
        newImg = exposure.equalize_adapthist(newImg, (300, 300))
        newImg = exposure.equalize_adapthist(newImg, (150, 150))
        #newImg = morphology.erosion(newImg)
        #newImg = filters.unsharp_mask(newImg, radius=10, amount=1)
        newImg = 1 - newImg

        #newImg = exposure.rescale_intensity(img, out_range=(0, 1))
        #newImg = ndi.binary_fill_holes(newImg)
        #newImg = newImg > filters.threshold_local(newImg, 99)
        #morphology.remove_small_objects(newImg, 250)
        newImg = filters.gaussian(newImg, sigma=3)
        newImg = newImg > filters.threshold_local(newImg, 21, method='generic', param=self.calc)
        newImg = morphology.remove_small_objects(newImg, 700)
        for i in range(len(newImg)):  # USUWANIE OBRĘCZY
            for j in range(len(newImg[0])):
                if (((i - 477) ** 2) + ((j - 494) ** 2)) ** 0.5 > 440:
                    newImg[i][j] = 0

        """newImg = filters.gaussian(newImg, sigma=3)
        newImg = filters.sobel(newImg)   # całkiem niezły wynik
        newImg = newImg > 0.045
        newImg = morphology.remove_small_objects(newImg, 250)"""

        self.resultPath = "result.png"
        newImg = img_as_float(newImg)
        io.imsave(self.resultPath, newImg)
        self.showResultingImage()
        self.analyzeResults(newImg)


    def advancedProcessing(self):
        tree_model = joblib.load("drzewko.pkl")
        pixelPerCell = 9
        newImg = classify(self.imagePath, tree_model, pixelPerCell)
        self.resultPath = "result.png"
        newImg = img_as_float(newImg)
        io.imsave(self.resultPath, newImg)
        self.showResultingImage()
        self.analyzeResults(newImg)


    def analyzeResults(self, result):
        expertMask = io.imread(self.imagePath[:-4] + "_1stHO.png")
        expertMask = img_as_float(expertMask)
        mistakeMatrix = np.zeros((self.IMAGE_WIDTH, self.IMAGE_HEIGHT, 3))
        truePositive = trueNegative = falsePositive = falseNegative = positive = negative = 0
        for i in range(self.IMAGE_HEIGHT):
            for j in range(self.IMAGE_WIDTH):
                if expertMask[i][j] == 0:
                    negative += 1
                    if result[i][j] == 0:
                        trueNegative += 1
                    else:
                        falsePositive += 1
                        mistakeMatrix[i][j][1] = 1
                else:
                    positive += 1
                    if result[i][j] == 0:
                        falseNegative += 1
                        mistakeMatrix[i][j][0] = 1
                    else:
                        truePositive += 1
                        mistakeMatrix[i][j] = 1
        print(positive, negative, truePositive, trueNegative, falseNegative, falsePositive)
        accuracy = (truePositive + trueNegative) / self.NUM_OF_PIXELS
        sensitivity = truePositive / positive
        specificity = trueNegative / negative
        io.imsave("mistakes.png", mistakeMatrix)
        print("ACCURACY : " + str(accuracy) + "\nSENSITIVITY: " + str(sensitivity) + "\nSPECIFICITY: " + str(specificity))

    def calc(self, chunk):
        result = np.sum(chunk) / len(chunk)
        if result < 0.5:
            return result * 1.25
        else:
            return result + 0.05


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
