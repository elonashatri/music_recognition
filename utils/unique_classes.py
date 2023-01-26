# this is just for the sake of having a file that lists all possible classes with position

import re 

def get_unique_classes(file_path):
    # Open the file and read in the contents
    with open(file_path, 'r') as file:
        contents = file.read()
        contents = re.sub(r'\S+\.png', '', contents)
    # Split the contents into words
   
    classes = contents.split()
    # Create a set of unique words
    unique_classes = set(classes)
    # remove number_only_words from unique_words
    # unique_words = [word for word in unique_words if not word.isnumeric()]
    unique_classes = sorted(unique_classes)
    # Write the unique words to a new .txt file
    with open('/data/home/acw507/music_recognition/data/unqiue_classes.txt', 'w') as outfile:
        for word in unique_classes:
            # remove the last three characters of the class
            # word = word[:-3]
            outfile.write(word + '\n')
    return unique_classes


unique_classes = get_unique_classes('/data/home/acw507/music_recognition/data/GT.txt')