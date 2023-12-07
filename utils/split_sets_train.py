## allocating train, test and validate datasets
import random 

fin = open('/data/home/acw507/music_recognition/data/original_data/GT.txt', 'rb') 
f75out = open("/data/home/acw507/music_recognition/data/original_data/train.txt", 'wb') 
f125aout = open("/data/home/acw507/music_recognition/data/original_data/test.txt", 'wb')
f125bout = open("/data/home/acw507/music_recognition/data/original_data/valid.txt", 'wb')

# change values for the splits for train, valdiation and test GT files
for line in fin: 
  r = random.random() 
  if (0.0 <=  r <= 0.70): 
    f75out.write(line) 
  elif (0.75 < r <= 0.80): 
    f125aout.write(line) 
  else:
    f125bout.write(line)
fin.close() 
f75out.close() 
f125aout.close() 
f125bout.close() 