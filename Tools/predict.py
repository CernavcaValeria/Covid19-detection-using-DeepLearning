
import cv2
from subprocess import call
import numpy as np
from os import listdir
import tensorflow as tensorflow




def normalization(images):
    #to 1 or to 0
    images = images/255.0
    return images



def editImage(image,imgDim):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (imgDim, imgDim))
    return image



def dataTo2d(image):
    imageDimenssion = 244
    retImgTo2d = np.array(image).reshape(-1, imageDimenssion, imageDimenssion, 3)
    return retImgTo2d


def reshapeImageForNN(image):
    imgSize=244
    image = np.reshape(image,[imgSize* imgSize*3,1])
    image = image.reshape(1,imgSize,imgSize,3).astype('float')
    return image


def prepareImageForPrediction(folder):
    for imageName in listdir(folder):
        imagePath = folder + "/" + imageName
        image = cv2.imread(imagePath)
    imageEdit = editImage(image,244)
    npImageEdited = np.array(imageEdit)
    to2DImage = dataTo2d(npImageEdited)
    imageNormalzd = normalization(to2DImage)
    return imageNormalzd


def loadModel():
    loadedModel = tensorflow.keras.models.load_model("Tools/model.h5")
    return loadedModel


imageForTest = prepareImageForPrediction("Image")

model = loadModel()
probabilityOfPrediction = model.predict(imageForTest, verbose=1)
probabilityOfPredictionTolist = probabilityOfPrediction.tolist()[0]


text = open("Tools/probability.txt", "w")
text.write("Covid:\n")
text.write("%f\n" % probabilityOfPredictionTolist[0])
text.write("Normal:\n")
text.write("%f\n" % probabilityOfPredictionTolist[1])
text.close()






"""
with open('Tools/probJson.json', 'w') as jsonFile:
    json.dump({'covid': probabilityOfPredictionTolist[0],
               'normal': probabilityOfPredictionTolist[1] }, jsonFile)

probabilitiesJson = {
    'covid': probabilityOfPredictionTolist[0],
    'normal': probabilityOfPredictionTolist[1]
}

with open('probJson.json', 'w') as jsonFile:
    json.dump(probabilitiesJson, jsonFile)


with open("probability.txt", "w") as text:
    for elem in probabilityOfPredictionTolist:
        text.write("%f\n" % elem)
    #print(characheter)      
text.close()


text = open("probability.txt", "w")
text.write(probabilityOfPredictionTolist[0])
text.write(probabilityOfPredictionTolist[1])
text.close()

with open("probability.txt", "w") as text:

    probabilities = probabilityOfPredictionTolist
    for characheter in probabilities:
        #print(characheter)
        
text.close()
"""