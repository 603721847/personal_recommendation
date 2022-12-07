train_file=train.txt
./bin/word2vec -train $train_file -output item_vec.txt -size 128 -window 5 -sample 1e-3 -negative  -5 -hs 0 -binary 0 -cbow 0 -iter 10