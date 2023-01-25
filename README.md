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
    CUDA_VISIBLE_DEVICES=0 python3 train.py \
        --train_data data_lmdb_release/training --valid_data data_lmdb_release/validation \
        --select_data MJ-ST --batch_ratio 0.5-0.5 \
        --Transformation None --FeatureExtraction VGG --SequenceModeling BiLSTM --Prediction CTC

or to test:

    CUDA_VISIBLE_DEVICES=0 python3 test.py \
        --eval_data data_lmdb_release/evaluation --benchmark_all_eval \
        --Transformation None --FeatureExtraction VGG --SequenceModeling BiLSTM --Prediction CTC \
        --saved_model saved_models/None-VGG-BiLSTM-CTC-Seed1111/best_accuracy.pth

or for a different model architecture:

    CUDA_VISIBLE_DEVICES=0 python3 train.py \
        --train_data data_lmdb_release/training --valid_data data_lmdb_release/validation \
        --select_data MJ-ST --batch_ratio 0.5-0.5 \
        --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn

testing:

    CUDA_VISIBLE_DEVICES=0 python3 test.py \
            --eval_data data_lmdb_release/evaluation --benchmark_all_eval \
            --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn \
            --saved_model saved_models/TPS-ResNet-BiLSTM-Attn-Seed1111/best_accuracy.pth


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