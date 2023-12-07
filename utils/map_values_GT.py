class_codes = {}

with open("/data/home/acw507/music_recognition/data/original_data/encoded_classes_dictionary.txt", "r") as file:
    for line in file:
        classname, class_code = line.strip().split(",")
        class_codes[classname] = class_code

with open("/data/home/acw507/music_recognition/data/original_data/GT.txt", "r") as file:
    data = file.read()

for classname, class_code in class_codes.items():
    data = data.replace(classname, class_code)

with open("/data/home/acw507/music_recognition/data/original_data/encoded_GT_agnostic.txt", "w") as file:
    file.write(data)
