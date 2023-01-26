""" a modified version of CRNN torch repository https://github.com/bgshih/crnn/blob/master/tool/create_dataset.py 
I change the paths where to look for the GT files and the images only"""
import fire
import os
import lmdb
import cv2
import pandas as pd
import numpy as np

def checkImageIsValid(imageBin):
    if imageBin is None:
        return False
    imageBuf = np.frombuffer(imageBin, dtype=np.uint8)
    img = cv2.imdecode(imageBuf, cv2.IMREAD_GRAYSCALE)
    imgH, imgW = img.shape[0], img.shape[1]
    if imgH * imgW == 0:
        return False
    return True


# switched to str(k).encode(), str(v).encode() so it doesn't read it as list but bytelike

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



if __name__ == '__main__':
    fire.Fire(createDataset)


"""Running it you need three different arguments:
1. inputPath: the path where the images are stored
2. gtFile: the path to the file with the ground truth
3. outputPath: the path where the lmdb file will be stored"""

"""Some of my path examples
python create_lmdb_dataset.py --inputPath /data/scratch/acw507/Corpus \
    --gtFile /data/home/acw507/music_recognition/data/tiny_dataset/valid.txt \
    --outputPath /data/home/acw507/music_recognition/data/tiny_dataset/valid
"""