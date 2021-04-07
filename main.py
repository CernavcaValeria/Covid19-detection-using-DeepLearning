
import os
import sys
import cv2
import random
import path
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
import tensorflow as tensorflow
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications import VGG19
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.applications import Xception
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


def normalization(images):
    #to 1 or to 0
    images = images/255.0
    return images



def editImage(image,imgDim):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (imgDim, imgDim))
    return image



def getClassesName(dataSetFolderName):
    pathName = "./"+dataSetFolderName
    listOfDictClasses = []
    for directory in listdir(pathName):
        pathOfCurrentClass = pathName + "/" + directory
        tempList = []
        tempList.append([str(directory)])
        tempList.append(str(pathOfCurrentClass))
        listOfDictClasses.append(tempList)
    return listOfDictClasses



def dataTo2d(dataset):
    imageDimenssion = 244
    retImgListTo2d = np.array([index[0] for index in dataset]).reshape(-1, imageDimenssion, imageDimenssion, 3)
    retCorrespondentClass = np.array([index[1] for index in dataset])
    return retImgListTo2d, retCorrespondentClass



def oneHotEncodeClasses(listOfClasses):
    oneHotEncClasses = []
    encodingForHealthy = np.array([1,0], dtype=float)
    encodingForCovid = np.array([0,1], dtype=float)

    for className in listOfClasses:
        if className[0]=='healthy':
            oneHotEncClasses.append(encodingForHealthy)
        elif className[0]=='covid':
            oneHotEncClasses.append(encodingForCovid)
    return oneHotEncClasses



def displayImage(data, itsClass, pos=0):
    plt.imshow(data[pos])
    print ("CLASS = " + str(np.squeeze(itsClass[pos])))
    print ("Image size: ",data[pos].shape)



def displayDims(imgSet,classesSet):
  print("Shape of images: ", imgSet.shape)
  print("Shape of classes: ", classesSet.shape)



def hotEcodeClass(listClasses):
    labelBinarizer = LabelBinarizer()
    bynaryClassName = labelBinarizer.fit_transform(listClasses)
    oneHotEncClassTrain = to_categorical(bynaryClassName)
    
    return oneHotEncClassTrain



def splitDataInTrainAnTest(listOfImgAnditsClass, proportion):
    lenght = len(listOfImgAnditsClass)
    proportionSize = int((lenght)*proportion)

    dataListForTesting = []
    dataListForTraining = listOfImgAnditsClass

    indexesList = []
    counter = 0
    while len(indexesList)<proportionSize:
        index = random.randint(0,(lenght-1))
        if counter==0:
            dataListForTesting.append(listOfImgAnditsClass[index])
            indexesList.append(index)
            counter+=1
        elif counter>0:
            if index not in indexesList:
                dataListForTesting.append(listOfImgAnditsClass[index])
                indexesList.append(index)

    indexesList.sort(reverse=True)
    for poz in indexesList:
        dataListForTraining.pop(poz)

    return (dataListForTraining, dataListForTesting)
    



def getDatasAndItsClasses(dataSetFolderName):
    listOfDictOfClasses = getClassesName(dataSetFolderName)
    imageDimenssion = 244
    Images = []
    for element in listOfDictOfClasses:
        className = element[0]
        classPath = element[1]
        for imageName in listdir(classPath):
            imagePath = classPath + "/" + imageName
            image = cv2.imread(imagePath)
            imageEdited = editImage(image,imageDimenssion)
            Images.append([np.array(imageEdited),className])

    imageForArchive = []
    clasesForArchive = []
    random.shuffle(Images)
    for element in Images:
        imageForArchive.append(element[0])
        clasesForArchive.append(element[1])
    archiveUnion = [imageForArchive, clasesForArchive]

    return (Images, archiveUnion)



def prepareData(trainDataSet ,testDataSet):

    trainDataTo2d, trainCorespClassTo2d = dataTo2d(trainDataSet)
    testDataTo2d, testCorespClassTo2d = dataTo2d(testDataSet)
    
    dataTrainNormalized = normalization(trainDataTo2d)
    dataTestNormalized = normalization(testDataTo2d)
    
    oneHotEncClassTrain = hotEcodeClass(trainCorespClassTo2d)
    oneHotEncClassTeste = hotEcodeClass(testCorespClassTo2d)
    """
    first = trainDataSet[0]
    classOfFirstTrianDatat = first[1]
    
    print("\n\n\n\nClass",classOfFirstTrianDatat)
    print("hotEndonding forFirst train Data:",oneHotEncClassTrain[0])
    #own onehotenc function
    #oneHotEncClassTrain = oneHotEncodeClasses(trainCorespClassTo2d)
    #oneHotEncClassTeste = oneHotEncodeClasses(testCorespClassTo2d)
    """
    return (dataTrainNormalized, dataTestNormalized, oneHotEncClassTrain, oneHotEncClassTeste )




listOfImgAnditsClass,Archive = getDatasAndItsClasses("dataBase")

#impart pozele pentru antrenare 80% ; pentru testare 20%
(trainDataSet ,testDataSet) = splitDataInTrainAnTest(listOfImgAnditsClass, 0.20)
(trainData ,testData, trainCorespClass, testCorespClass) = prepareData(trainDataSet ,testDataSet)



#display distribution
displayDims(trainData , trainCorespClass)
displayDims(testData, testCorespClass)



#init learning rate, epochs number, batch size
learningRate = 1e-3
epochs = 15
bachSize = 8


#retea neuronala preantrenata 
baseModel = DenseNet121(weights= "imagenet",
                include_top=False,
                input_tensor=Input(shape=(244,244,3)))


#construiesc capul modelului ce va fi plasat in modelul de baza

mainModel = baseModel.output

mainModel = AveragePooling2D(pool_size=(4,4))(mainModel)

mainModel = Flatten(name="flatten")(mainModel)

mainModel = Dense(64, activation = "relu")(mainModel)

mainModel = Dropout(0.5)(mainModel)

mainModel = Dense(2,activation = "softmax")(mainModel)


model = Model(inputs=baseModel.input, outputs=mainModel)


#bucla peste toate layerele din baseModel, 
#ca si cum le-am ingheta pt ca ele sa nu se updatetze in timpul primului proces de antrenare
for layer in baseModel.layers:
    layer.trainable = False


#compile model,info about compiling
optimizerAdam = Adam(lr=learningRate,decay=(learningRate/epochs))
model.compile(loss="binary_crossentropy",
                optimizer = optimizerAdam,
                metrics=[tensorflow.keras.metrics.SpecificityAtSensitivity(0.5), 'accuracy'] )


print("Training ...")
tranedModel = model.fit(    trainData , 
                            trainCorespClass,
                            batch_size = bachSize,
                            steps_per_epoch=len(trainData)//bachSize,
                            validation_data=(testData, testCorespClass),
                            validation_steps=len(testData)//bachSize,
                            epochs=epochs )


model.evaluate(testData,verbose=1)

# serialize weights to H5
model.save("Models/DenseNet121.h5")
print("Modelul salvat cu succes")

plt.plot(tranedModel.history['accuracy'],color='blue')
plt.plot(tranedModel.history['val_accuracy'],color = 'green')
plt.title('Model DenseNet121: Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='lower right')
plt.show()
# summarize history for loss
plt.plot(tranedModel.history['loss'], color = 'red' )
plt.plot(tranedModel.history['val_loss'],color = 'orange')
plt.title('Model DenseNet121: Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()

# summarize history for loss-acc
plt.plot(tranedModel.history['accuracy'],color='blue')
plt.plot(tranedModel.history['val_accuracy'],color = 'green')
plt.plot(tranedModel.history['loss'], color = 'red' )
plt.plot(tranedModel.history['val_loss'],color = 'orange')
plt.title('Model DenseNet121')
plt.ylabel('Accuracy/Loss')
plt.xlabel('Epoch')
plt.legend(['trainAcc', 'testAcc','trainLoss','testLoss'], loc='lower left')
plt.show()