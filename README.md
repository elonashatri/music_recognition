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

The structure that is expected by create_lmdb_dataset.py is 

test/word_1.png Tiredness
test/word_2.png kills
test/word_3.png A
...


Now all data is ready we can start training from scratch, fine-tuning or just testing with the following commads:

    CUDA_VISIBLE_DEVICES=0 python3 /data/home/acw507/music_recognition/train.py \
        --train_data /data/home/acw507/music_recognition/data/train --valid_data /data/home/acw507/music_recognition/data/valid \
        --select_data train --batch_ratio 0.5 \
        --Transformation None --FeatureExtraction VGG --SequenceModeling BiLSTM --Prediction CTC

or to test:

    CUDA_VISIBLE_DEVICES=0 python3 /data/home/acw507/music_recognition/train.py \
        --train_data /data/home/acw507/music_recognition/data/train --valid_data /data/home/acw507/music_recognition/data/valid \
        --Transformation None --FeatureExtraction VGG --SequenceModeling BiLSTM --Prediction CTC \
        --saved_model saved_models/None-VGG-BiLSTM-CTC-Seed1111/best_accuracy.pth

or for a different model architecture:

    CUDA_VISIBLE_DEVICES=0 python3 /data/home/acw507/music_recognition/train.py \
        --train_data /data/home/acw507/music_recognition/data/train --valid_data /data/home/acw507/music_recognition/data/valid \
        --select_data MJ-ST --batch_ratio 0.5-0.5 \
        --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn

testing:

    CUDA_VISIBLE_DEVICES=0 python3 /data/home/acw507/music_recognition/train.py \
        --train_data /data/home/acw507/music_recognition/data/train --valid_data /data/home/acw507/music_recognition/data/valid \
        --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn \
        --saved_model saved_models/TPS-ResNet-BiLSTM-Attn-Seed1111/best_accuracy.pth


export LD_PRELOAD=/data/home/acw507/.conda/envs/pytorchenv/lib/libstdc++.so.6.0.29

<!-- # training testing on a tiny set 
    CUDA_VISIBLE_DEVICES=0 python3 /data/home/acw507/music_recognition/train.py \
        --train_data /data/home/acw507/music_recognition/data/tiny_dataset/train \
        --valid_data /data/home/acw507/music_recognition/data/tiny_dataset/valid \
        --select_data train --batch_ratio 0.5 \
        --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn

/data/home/acw507/music_recognition/data/tiny_dataset/train -->

Arguments:

        --train_data: folder path to training lmdb dataset.
        --valid_data: folder path to validation lmdb dataset.
        --eval_data: folder path to evaluation (with test.py) lmdb dataset.
        --select_data: select training data, choose train
        --batch_ratio: assign ratio for each selected data in the batch. default is 0.5
        --data_filtering_off: skip data filtering when creating LmdbDataset.
        --Transformation: select Transformation module [None | TPS].
        --FeatureExtraction: select FeatureExtraction module [VGG | RCNN | ResNet].
        --SequenceModeling: select SequenceModeling module [None | BiLSTM].
        --Prediction: select Prediction module [CTC | Attn].
        --saved_model: assign saved model to evaluation.
        --benchmark_all_eval: evaluate with other datasets


If problems with GCC export it from the right path:

    export LD_PRELOAD=/homes/es314/miniconda3/envs/bttr/lib/libstdc++.so.6.0.29 

Code is heavily based on https://github.com/clovaai/deep-text-recognition-benchmark