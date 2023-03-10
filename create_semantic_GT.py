"""Based on the script from https://github.com/antoniorv6/transformers_omr """
import cv2
import numpy as np
import os

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

            # get the corresponding semantic file name
            semantic_filename = f"{folder}.semantic"
            semantic_file_path = os.path.join(path, folder, semantic_filename)

            # read the contents of the semantic file
            with open(semantic_file_path, "r") as af:
                semantic_contents = af.read()
                if encoding == "standard":
                    Y.append(semantic_contents.strip().split("\t"))
                else:
                    splitted_seq = []
                    sequence = semantic_contents.strip().split("\t")
                    for element in sequence:
                        for char in element.split("-"):
                            splitted_seq.append(char)
                    Y.append(splitted_seq)

            # write the image filename and the semantic file contents to the output file
            f.write(f"{img_filename}\t")
            f.write(f"{semantic_contents}\n")

            if i > limit:
                break
            i+=1



loadPrimus('/data/scratch/acw507/Corpus/', 'semantic', '/data/home/acw507/music_recognition/data/semantic/GT_semantic.txt')

