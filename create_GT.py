"""Based on the script from https://github.com/antoniorv6/transformers_omr """
import json
import cv2
import numpy as np
import os
import sys
import tqdm
import glob

def loadPrimus(path, encoding, output_file):
    X=[]
    Y=[]
    limit = 100000
    i = 0 
    with open(output_file, "a") as f: # "a" is for appending instead of writing
        for folder in os.listdir(path):
            # get the image file name
            img_filename = f"{folder}.png"
            img_path = os.path.join(path, folder, img_filename)
            img = cv2.imread(img_path, 0)
            X.append(img)
            # print(img_path)

            # get the corresponding agnostic file name
            agnostic_filename = f"{folder}.agnostic"
            agnostic_file_path = os.path.join(path, folder, agnostic_filename)

            # read the contents of the agnostic file
            with open(agnostic_file_path, "r") as af:
                agnostic_contents = af.read()
                if encoding == "standard":
                    Y.append(agnostic_contents.strip().split("\t"))
                else:
                    splitted_seq = []
                    sequence = agnostic_contents.strip().split("\t")
                    for element in sequence:
                        for char in element.split("-"):
                            splitted_seq.append(char)
                    Y.append(splitted_seq)

            # write the image filename and the agnostic file contents to the output file
            f.write(f"{img_filename}\t")
            f.write(f"{agnostic_contents}\n")

            if i > limit:
                break
            i+=1



loadPrimus('/import/c4dm-05/elona/Corpus', 'agnostic', '/homes/es314/deep-text-recognition-benchmark/new_primus_clean/primus_whole_GT.txt')

