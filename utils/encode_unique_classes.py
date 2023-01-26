import os

class_codes = {}

with open("/data/home/acw507/music_recognition/data/unqiue_classes.txt", "r") as file:
    for index, classname in enumerate(file):
        classname = classname.strip()
        class_code = str(index + 1).zfill(3)
        class_codes[classname] = class_code

with open("/data/home/acw507/music_recognition/data/class_codes.txt", "w") as file:
    for classname, class_code in class_codes.items():
        file.write(f"{classname},{class_code}\n")
