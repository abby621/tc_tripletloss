# create the lmdbs
rm -r /project/focus/datasets/tc_tripletloss/small_triplet_test_lmdb
$CAFFE_ROOT/build/tools/convert_imageset --resize_height 227 --resize_width 227 / /project/focus/datasets/tc_tripletloss/small_test_triplets.txt /project/focus/datasets/tc_tripletloss/small_triplet_test_lmdb

rm -r /project/focus/datasets/tc_tripletloss/small_triplet_train_lmdb
$CAFFE_ROOT/build/tools/convert_imageset --resize_height 227 --resize_width 227 / /project/focus/datasets/tc_tripletloss/small_train_triplets.txt /project/focus/datasets/tc_tripletloss/small_triplet_train_lmdb

rm -r /project/focus/datasets/tc_tripletloss/triplet_test_lmdb
$CAFFE_ROOT/build/tools/convert_imageset --resize_height 227 --resize_width 227 / /project/focus/datasets/tc_tripletloss/test_triplets.txt /project/focus/datasets/tc_tripletloss/triplet_test_lmdb

rm -r /project/focus/datasets/tc_tripletloss/triplet_train_lmdb
$CAFFE_ROOT/build/tools/convert_imageset --resize_height 227 --resize_width 227 / /project/focus/datasets/tc_tripletloss/train_triplets.txt /project/focus/datasets/tc_tripletloss/triplet_train_lmdb

# overtrain to find good learning rate
screen -S lr01
GLOG_log_dir=/project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr01/ $CAFFE_ROOT/build/tools/caffe train -solver /project/focus/abby/tc_tripletloss/models/solvers/solver_lr01.prototxt -weights /project/focus/abby/tc_tripletloss/models/alexnet_places365.caffemodel -gpu 0
screen -S lr001
GLOG_log_dir=/project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr001/ $CAFFE_ROOT/build/tools/caffe train -solver /project/focus/abby/tc_tripletloss/models/solvers/solver_lr001.prototxt -weights /project/focus/abby/tc_tripletloss/models/alexnet_places365.caffemodel -gpu 1
screen -S lr0001
GLOG_log_dir=/project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0001/ $CAFFE_ROOT/build/tools/caffe train -solver /project/focus/abby/tc_tripletloss/models/solvers/solver_lr0001.prototxt -weights /project/focus/abby/tc_tripletloss/models/alexnet_places365.caffemodel -gpu 2
screen -S lr05
GLOG_log_dir=/project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr05/ $CAFFE_ROOT/build/tools/caffe train -solver /project/focus/abby/tc_tripletloss/models/solvers/solver_lr05.prototxt -weights /project/focus/abby/tc_tripletloss/models/alexnet_places365.caffemodel -gpu 3
screen -S lr005
GLOG_log_dir=/project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr005/ $CAFFE_ROOT/build/tools/caffe train -solver /project/focus/abby/tc_tripletloss/models/solvers/solver_lr005.prototxt -weights /project/focus/abby/tc_tripletloss/models/alexnet_places365.caffemodel -gpu 2
screen -S lr0005
GLOG_log_dir=/project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0005/ $CAFFE_ROOT/build/tools/caffe train -solver /project/focus/abby/tc_tripletloss/models/solvers/solver_lr0005.prototxt -weights /project/focus/abby/tc_tripletloss/models/alexnet_places365.caffemodel -gpu 1

# once they've run long enough to over train, close the screens
screen -X -S lr01 quit
screen -X -S lr001 quit
screen -X -S lr0001 quit
screen -X -S lr05 quit
screen -X -S lr005 quit
screen -X -S lr0005 quit

# if for some reason, we stop and start over again and need to delete the logs: rm /project/focus/abby/tc_tripletloss/models/logs/traffickcam/*/*

# parse logs and move them so that we can grab them to have unique names
$CAFFE_ROOT/tools/extra/parse_log.py /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr01/caffe.INFO /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr01/
mv /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr01/caffe.INFO.train /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr01/lr01.train
mv /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr01/caffe.INFO.test /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr01/lr01.test
$CAFFE_ROOT/tools/extra/parse_log.py /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr001/caffe.INFO /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr001/
mv /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr001/caffe.INFO.train /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr001/lr001.train
mv /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr001/caffe.INFO.test /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr001/lr001.test
$CAFFE_ROOT/tools/extra/parse_log.py /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0001/caffe.INFO /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0001/
mv /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0001/caffe.INFO.train /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0001/lr0001.train
mv /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0001/caffe.INFO.test /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0001/lr0001.test
$CAFFE_ROOT/tools/extra/parse_log.py /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr05/caffe.INFO /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr05/
mv /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr05/caffe.INFO.train /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr05/lr05.train
mv /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr05/caffe.INFO.test /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr05/lr05.test
$CAFFE_ROOT/tools/extra/parse_log.py /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr005/caffe.INFO /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr005/
mv /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr005/caffe.INFO.train /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr005/lr005.train
mv /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr005/caffe.INFO.test /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr005/lr005.test
$CAFFE_ROOT/tools/extra/parse_log.py /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0005/caffe.INFO /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0005/
mv /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0005/caffe.INFO.train /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0005/lr0005.train
mv /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0005/caffe.INFO.test /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0005/lr0005.test

# once we determine a good learning rate, update the solver to use 'train.prototxt' instead of 'overtrain.prototxt'
# train, storing log information
GLOG_log_dir=/project/focus/abby/tc_tripletloss/models/logs/traffickcam/ $CAFFE_ROOT/build/tools/caffe train -solver /project/focus/abby/tc_tripletloss/models/solver.prototxt -weights /project/focus/abby/tc_tripletloss/models/alexnet_places365.caffemodel -gpu 0
# parse logs
$CAFFE_ROOT/tools/extra/parse_log.py /project/focus/abby/tc_tripletloss/models/logs/traffickcam/caffe.INFO /project/focus/abby/tc_tripletloss/models/logs/traffickcam/
