import numpy as np
import cv2
from PIL import Image, ImageStat
from scipy import ndimage
from sklearn import tree
from sklearn.model_selection import cross_val_score, GridSearchCV
import joblib
from skimage import data, exposure, io, color, img_as_float, filters, morphology
import random

def addImage(dataFilename, maskFilename, pixelPerCell):
    countTrue, countFalse = 0, 0
    dataIm = np.array(Image.open(dataFilename)) #you can pass multiple arguments in single line\n",
    maskIm = np.array(Image.open(maskFilename)) #you can pass multiple arguments in single line\n",
    dataGrey = dataIm[:,:,:]
    dataGrey[:,:,0] = 0 # PREPROCESSING
    dataGrey[:,:,2] = 0
    dataGrey = color.rgb2gray(dataGrey)
    dataGrey = exposure.equalize_adapthist(dataGrey)
    dataGrey = exposure.equalize_adapthist(dataGrey, (50, 50))
    dataGrey = exposure.equalize_adapthist(dataGrey, (300, 300))
    dataGrey = exposure.equalize_adapthist(dataGrey, (150, 150))
    #dataGrey = np.where((1 - dataGrey) < 80/255, 1, dataGrey + 80/255)

    #dataGrey = filters.gaussian(dataGrey, sigma=2)
    margin = pixelPerCell-pixelPerCell//2
    translation = pixelPerCell//2
    chosen =[]
    result = np.where(maskIm == True)
    isChecked = np.zeros((dataIm.shape[0], dataIm.shape[1]))
    while countTrue < 50000:
        i = random.randrange(15, dataIm.shape[0] - 15)
        j = random.randrange(15, dataIm.shape[1] - 15)
        if isChecked[i][j] > 0:
            continue
        isChecked[i][j] = 1
        if (((i - 477) ** 2) + ((j - 494) ** 2)) ** 0.5 > 475:
            continue
        if maskIm[i][j] == False and countFalse > countTrue:
            continue
        subData = [] #tablica na parametry obliczone dla komórki\n",
        #***skopiowanie fragmentu obrazu\n",
        subImage = dataIm[i-translation:i+translation+1,j-translation:j+translation+1,:]
        varianceG = ndimage.measurements.variance(subImage[:, :, 1])
        subData.append((dataIm[i][j][0]+dataIm[i][j][1] + dataIm[i][j][2])/3)
        subData.append(varianceG)
        #***PREPROCESSING
        subImage = dataGrey[i-pixelPerCell*2:i+pixelPerCell*2+1,j-pixelPerCell*2:j+pixelPerCell*2+1]
        # ***obliczanie momentów Hu
        subData.append(np.sum(subImage) / np.size(subImage))
        # #***zapisanie zgromadzonych danych\n",
        #if subData not in data['data']:
        data['data'].append(subData)
        #***dodanie decyzji z maski eksperckiej\n",
        data['mask'].append(maskIm[i][j])
        if maskIm[i][j] == True:
            countTrue += 1
        else:
            countFalse += 1


data = {}
data['data'] = []
data['mask'] = []

pixelPerCell = 9


addImage('Image_02L.jpg', 'Image_02L_1stHO.png', pixelPerCell)
addImage('Image_04L.jpg', 'Image_04L_1stHO.png', pixelPerCell)
addImage('Image_06L.jpg', 'Image_06L_1stHO.png', pixelPerCell)
addImage('Image_14L.jpg', 'Image_14L_1stHO.png', pixelPerCell)
print("ALLADDED")

x = data['data']
y = data['mask']
parameters = {'max_depth':range(5,11)}
clf = GridSearchCV(tree.DecisionTreeClassifier(random_state=0), parameters, n_jobs=1, scoring=['accuracy', 'precision', 'recall'], refit = 'accuracy')
clf.fit(X=x, y=y)
tree_model = clf.best_estimator_
print (clf.best_score_, clf.best_params_)

joblib.dump(tree_model, "drzewko.pkl")