import numpy as np
import cv2
from PIL import Image, ImageStat
from scipy import ndimage
from sklearn import tree
from sklearn.model_selection import cross_val_score, GridSearchCV
import joblib
from skimage import data, exposure, io, color, img_as_float, filters

def addImage(dataFilename, maskFilename, pixelPerCell):
    countTrue, countFalse = 0, 0
    dataIm = np.array(Image.open(dataFilename)) #you can pass multiple arguments in single line\n",
    gamma=1.5# Gamma < 1 ~ Dark ; Gamma > 1 ~ Bright
    dataIm=((dataIm/255)**(1/gamma))
    maskIm = np.array(Image.open(maskFilename)) #you can pass multiple arguments in single line\n",
    dataGrey = dataIm[:,:,:]
    #dataGrey[:,:,0] = 0 # PREPROCESSING
    dataGrey[:,:,2] = 0
    dataGrey = color.rgb2gray(dataGrey)
    dataGrey = exposure.equalize_adapthist(dataGrey)
    dataGrey = exposure.equalize_adapthist(dataGrey, (50, 50))
    dataGrey = exposure.equalize_adapthist(dataGrey, (300, 300))
    dataGrey = exposure.equalize_adapthist(dataGrey, (150, 150))
    dataGrey = np.where((1 - dataGrey) < 80/255, 1, dataGrey + 80/255)
    #dataGrey = filters.gaussian(dataGrey, sigma=2)
    margin = pixelPerCell-pixelPerCell//2
    translation = pixelPerCell//2
    for i in range(margin, maskIm.shape[0] - margin - 1, 3):
        for j in range(margin, maskIm.shape[1] - margin - 1):#, translation-1):
            if (((i - 477) ** 2) + ((j - 494) ** 2)) ** 0.5 > 465:
                continue
            if maskIm[i][j] == False and countFalse > 2*countTrue:
                continue
            subData = [] #tablica na parametry obliczone dla komórki\n",
        #print(positionX, positionY)\n",
        #***skopiowanie fragmentu obrazu\n",
            subImage = dataIm[i-translation:i+translation+1,j-translation:j+translation+1,:]
            varianceR = ndimage.measurements.variance(subImage[:, :, 0])
            varianceG = ndimage.measurements.variance(subImage[:, :, 1])
            subData.append(varianceR)
            subData.append(varianceG)
            #stat = ImageStat.Stat(Image.fromarray(subImage).convert('L'))
            #subData.append(stat.mean[0])
            #***PREPROCESSING
            subImage = dataGrey[i-translation:i+translation+1,j-translation:j+translation+1]
            #***obliczanie momentów Hu
            moments = cv2.moments(subImage)
            huMoments = cv2.HuMoments(moments)
            #centralMoments = cv2.central_moments(subImage)
            #print(moments)\n",
            #print(huMoments)\n",
            #cy, cx = ndimage.center_of_mass(subImage)
            #subData.extend((cy, cx))
            #for m in huMoments:
            #    subData.append(m[0])
            subData.extend((huMoments[0][0], huMoments[3][0], huMoments[6][0]))
            #print(subData)\n",
            #***zapisanie zgromadzonych danych\n",
            if subData not in data['data']:
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
addImage('Image_01L.jpg', 'Image_01L_1stHO.png', pixelPerCell)
#addImage('Image_04L.jpg', 'Image_04L_1stHO.png', pixelPerCell)
addImage('Image_04R.jpg', 'Image_04R_1stHO.png', pixelPerCell)

x = data['data']
y = data['mask']
parameters = {'max_depth':range(4,8)}#, 'max_features':range(3,7)}
clf = GridSearchCV(tree.DecisionTreeClassifier(), parameters, n_jobs=-1, scoring=['recall', 'accuracy', 'precision'], refit = 'accuracy')
clf.fit(X=x, y=y)
tree_model = clf.best_estimator_
print (clf.best_score_, clf.best_params_)

joblib.dump(tree_model, "drzewko1.pkl")