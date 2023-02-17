import json
import cv2
import numpy as np
import os
import sys
import tqdm
import glob


def get_words(file_path):
    # Open the file and read in the contents
    with open(file_path, 'r') as file:
        contents = file.read()
        
    # Split the contents into words
    words = contents.split()
    with open('/data/home/acw507/music_recognition/data/only_position/only_position_GT.txt', 'w') as outfile:
        for word in words:
            if '/' in word:
                word = word.replace('/', '')
            if word.endswith(".png"):
                outfile.write('\n')
                word=word
            else:
                word = word[word.find('-'):]
            outfile.write(word + ' ')

    return words

words = get_words('/data/home/acw507/music_recognition/data/GT.txt')
