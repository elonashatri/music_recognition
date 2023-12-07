""" a modified version of CRNN torch repository https://github.com/bgshih/crnn/blob/master/tool/create_dataset.py 
I change the paths where to look for the GT files and the images only"""
import fire
import os
import lmdb
import cv2
import pandas as pd
import numpy as np
import random

def split_gt_file(gtFile, train_ratio=0.7, valid_ratio=0.2):
    with open(gtFile, 'r', encoding='utf-8') as data:
        datalist = data.readlines()

    random.shuffle(datalist)

    n_train = int(len(datalist) * train_ratio)
    n_valid = int(len(datalist) * valid_ratio)

    train_data = datalist[:n_train]
    valid_data = datalist[n_train:n_train + n_valid]
    test_data = datalist[n_train + n_valid:]

    with open("train.txt", "w", encoding="utf-8") as train_file:
        train_file.writelines(train_data)

    with open("valid.txt", "w", encoding="utf-8") as valid_file:
        valid_file.writelines(valid_data)

    with open("test.txt", "w", encoding="utf-8") as test_file:
        test_file.writelines(test_data)

    return "train.txt", "valid.txt", "test.txt"


def checkImageIsValid(imageBin):
    if imageBin is None:
        return False
    imageBuf = np.frombuffer(imageBin, dtype=np.uint8)
    img = cv2.imdecode(imageBuf, cv2.IMREAD_GRAYSCALE)
    imgH, imgW = img.shape[0], img.shape[1]
    if imgH * imgW == 0:
        return False
    return True


def writeCache(env, cache):
    with env.begin(write=True) as txn:
        for k, v in cache.items():
            txn.put(k, v)

def createDataset(inputPath, gtFile, outputPath, checkValid=True):
    """
    Create LMDB dataset for training and evaluation.
    ARGS:
        inputPath  : input folder path where starts imagePath
        outputPath : LMDB output path
        gtFile     : list of image path and label
        checkValid : if true, check the validity of every image
    """
    os.makedirs(outputPath, exist_ok=True)
    env = lmdb.open(outputPath, map_size=1099511627776)
    cache = {}
    cnt = 1

    with open(gtFile, 'r', encoding='utf-8') as data:
        datalist = data.readlines()

    nSamples = len(datalist)
    for i in range(nSamples):
        #changed the way it is reading the file so it reads the whole sequence after the image file name
        names =  datalist[i].strip().split()
        images = names[0]
        label = names[1:]
        label = ' '.join(set(label))
        # print(label)

        # added .jpg so we read the filename without extension in case we want to change the extesnions
        folder = images[:-4] #remove .png for the folder path since it is nestewd
        imagePath = os.path.join(inputPath, folder , images)

        if not os.path.exists(imagePath):
            print('%s does not exist' % imagePath)
            continue
        with open(imagePath, 'rb') as f:
            imageBin = f.read()
        if checkValid:
            try:
                if not checkImageIsValid(imageBin):
                    print('%s is not a valid image' % imagePath)
                    continue
            except:
                print('error occured', i)
                with open(outputPath + '/error_image_log.txt', 'a') as log:
                    log.write('%s-th image data occured error\n' % str(i))
                continue

        imageKey = 'image-%09d'.encode() % cnt
        labelKey = 'label-%09d'.encode() % cnt
        # print(labelKey)
        cache[imageKey] = imageBin
        cache[labelKey] = label.encode()
        # print(cache)




        if cnt % 10000 == 0:
            writeCache(env, cache)
            cache = {}
            print('Written %d / %d' % (cnt, nSamples))
        cnt += 1
    nSamples = cnt-1
    cache['num-samples'.encode()] = str(nSamples).encode()
    writeCache(env, cache)
    print('Created dataset with %d samples' % nSamples)



# if __name__ == '__main__':
#     fire.Fire(createDataset)


"""Running it you need three different arguments:
1. inputPath: the path where the images are stored
2. gtFile: the path to the file with the ground truth
3. outputPath: the path where the lmdb file will be stored"""

"""Some of my path examples
--inputPath /import/c4dm-05/elona/Corpus
--gtFile /import/c4dm-05/elona/primus_experiments/no-encoding/data/test.txt
--outputPath /import/c4dm-05/elona/primus_experiments/no-encoding/data/test
"""


if __name__ == '__main__':
    gtFile = "/data/home/acw507/music_recognition/data/original_data/GT.txt"
    inputPath = "/data/home/acw507/Corpus"
    outputPath = "/data/home/acw507/music_recognition/data/original_data"

    train_gtFile, valid_gtFile, test_gtFile = split_gt_file(gtFile)

    createDataset(inputPath, train_gtFile, os.path.join(outputPath, "train"))
    createDataset(inputPath, valid_gtFile, os.path.join(outputPath, "valid"))
    createDataset(inputPath, test_gtFile, os.path.join(outputPath, "test"))

    os.remove(train_gtFile)
    os.remove(valid_gtFile)
    os.remove(test_gtFile)