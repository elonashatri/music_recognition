class_codes = {}

with open("./data/class_codes.txt", "r") as file:
    for line in file:
        classname, class_code = line.strip().split(",")
        class_codes[classname] = class_code

with open("./data/tiny_dataset/testing_GT.txt", "r") as file:
    data = file.read()

for classname, class_code in class_codes.items():
    data = data.replace(classname, class_code)

with open("./data/tiny_dataset/testing_GT_encoded.txt", "w") as file:
    file.write(data)
