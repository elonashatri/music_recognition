We start by preparing the Ground truth files for train, valid and test. Depending on how your grountruth labels are saved different ways to grab it are needed. In my case I have the following structure for my files

    /import/c4dm-05/elona/Corpus/000051650-1_1_1 \
        --------/000051650-1_1_1_distorted.jpg \
        --------/000051650-1_1_1/000051650-1_1_1.agnostic \
        --------/000051650-1_1_1.mei \
        --------/000051650-1_1_1.png \ 
        --------/000051650-1_1_1.semantic \
    ...

The images that I want to use are the .png and the GT files are .agnostic

To walk through the whole Corpus folder into the subfolders that hold the images and GT I run this file:

        python create_GT.py

Next we have to split train, test and valid sets. 

        python split_sets_train.py 

Now we can create the lmdb encoded files which will then be used for training, validating and testing. Specify --input_path where the images are located, test/train or valid grountruth label txt and the path where you want the files saved. Create test/train/valid directories beforehand so you don't override any file. 

        python create_lmdb_dataset.py --inputPath /import/c4dm-05/elona/Corpus \    
                    --gtFile /import/c4dm-05/elona/primus_experiments/no-encoding/data/test.txt
                    --outputPath /import/c4dm-05/elona/primus_experiments/no-encoding/data/test


