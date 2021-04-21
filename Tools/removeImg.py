import os
from os import listdir

def delete(folder):
    for imageName in listdir(folder):
        imagePath = folder + "/" + imageName
        os.remove(imagePath)

delete("Image")