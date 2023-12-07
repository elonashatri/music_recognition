

def read_classes(file_path):
    with open(file_path, 'r') as file:
        classes = [line.strip() for line in file.readlines()]
    return classes

def encode_classes(classes):
    encoded_classes = {class_name: index for index, class_name in enumerate(classes)}
    return encoded_classes

def save_encoded_classes(file_path, encoded_classes):
    with open(file_path, 'w') as file:
        for class_name, index in encoded_classes.items():
            file.write(f'{class_name},{index}\n')

def main():
    input_file = '/data/home/acw507/music_recognition/data/original_data/unique_classes.txt'
    output_file = '/data/home/acw507/music_recognition/data/original_data/encoded_classes_dictionary.txt'

    classes = read_classes(input_file)
    encoded_classes = encode_classes(classes)
    save_encoded_classes(output_file, encoded_classes)

if __name__ == "__main__":
    main()
