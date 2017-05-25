WHICH_DATASET = 'mnist'

if WHICH_DATASET == 'tc':
    TARGET_SIZE = 227
    CROP_SZ = 227
    TRAIN_BATCH_SIZE = 30
    TEST_BATCH_SIZE = 30
    # GLOG_log_dir=/project/focus/abby/tc_tripletloss/models/logs/tc/ $CAFFE_ROOT/build/tools/caffe train -solver /project/focus/abby/tc_tripletloss/models/solver.prototxt -weights /project/focus/abby/tc_tripletloss/models/alexnet_places365.caffemodel -gpu 0
elif WHICH_DATASET == 'mnist':
    TARGET_SIZE = 28
    CROP_SZ = 28
    TRAIN_BATCH_SIZE = 270
    TEST_BATCH_SIZE = 270
    # GLOG_log_dir=/project/focus/abby/tc_tripletloss/models/logs/mnist/ $CAFFE_ROOT/build/tools/caffe train -solver /project/focus/abby/tc_tripletloss/models/solver.prototxt -weights /project/focus/abby/tc_tripletloss/models/mnist_pretrained.caffemodel -gpu 0
