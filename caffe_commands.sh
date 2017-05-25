rm -r /project/focus/datasets/tc_tripletloss/small_triplet_test_lmdb
$CAFFE_ROOT/build/tools/convert_imageset --resize_height 227 --resize_width 227 / /project/focus/datasets/tc_tripletloss/small_test_triplets.txt /project/focus/datasets/tc_tripletloss/small_triplet_test_lmdb

rm -r /project/focus/datasets/tc_tripletloss/small_triplet_train_lmdb
$CAFFE_ROOT/build/tools/convert_imageset --resize_height 227 --resize_width 227 / /project/focus/datasets/tc_tripletloss/small_train_triplets.txt /project/focus/datasets/tc_tripletloss/small_triplet_train_lmdb

rm -r /project/focus/datasets/tc_tripletloss/triplet_test_lmdb
$CAFFE_ROOT/build/tools/convert_imageset --resize_height 227 --resize_width 227 / /project/focus/datasets/tc_tripletloss/test_triplets.txt /project/focus/datasets/tc_tripletloss/triplet_test_lmdb

rm -r /project/focus/datasets/tc_tripletloss/triplet_train_lmdb
$CAFFE_ROOT/build/tools/convert_imageset --resize_height 227 --resize_width 227 / /project/focus/datasets/tc_tripletloss/train_triplets.txt /project/focus/datasets/tc_tripletloss/triplet_train_lmdb

# overtrain to find good learning rate
GLOG_log_dir=/project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr01/ $CAFFE_ROOT/build/tools/caffe train -solver /project/focus/abby/tc_tripletloss/models/solvers/solver_lr01.prototxt -weights /project/focus/abby/tc_tripletloss/models/alexnet_places365.caffemodel -gpu 0
GLOG_log_dir=/project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr001/ $CAFFE_ROOT/build/tools/caffe train -solver /project/focus/abby/tc_tripletloss/models/solvers/solver_lr001.prototxt -weights /project/focus/abby/tc_tripletloss/models/alexnet_places365.caffemodel -gpu 0
GLOG_log_dir=/project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0001/ $CAFFE_ROOT/build/tools/caffe train -solver /project/focus/abby/tc_tripletloss/models/solvers/solver_lr0001.prototxt -weights /project/focus/abby/tc_tripletloss/models/alexnet_places365.caffemodel -gpu 0
GLOG_log_dir=/project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr05/ $CAFFE_ROOT/build/tools/caffe train -solver /project/focus/abby/tc_tripletloss/models/solvers/solver_lr05.prototxt -weights /project/focus/abby/tc_tripletloss/models/alexnet_places365.caffemodel -gpu 0
GLOG_log_dir=/project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr005/ $CAFFE_ROOT/build/tools/caffe train -solver /project/focus/abby/tc_tripletloss/models/solvers/solver_lr005.prototxt -weights /project/focus/abby/tc_tripletloss/models/alexnet_places365.caffemodel -gpu 0
GLOG_log_dir=/project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0005/ $CAFFE_ROOT/build/tools/caffe train -solver /project/focus/abby/tc_tripletloss/models/solvers/solver_lr0005.prototxt -weights /project/focus/abby/tc_tripletloss/models/alexnet_places365.caffemodel -gpu 0

# parse logs
$CAFFE_ROOT/tools/extra/parse_log.py /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr01/caffe.INFO /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr01/
$CAFFE_ROOT/tools/extra/parse_log.py /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr001/caffe.INFO /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr001/
$CAFFE_ROOT/tools/extra/parse_log.py /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0001/caffe.INFO /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0001/
$CAFFE_ROOT/tools/extra/parse_log.py /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr05/caffe.INFO /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr05/
$CAFFE_ROOT/tools/extra/parse_log.py /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr005/caffe.INFO /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr005/
$CAFFE_ROOT/tools/extra/parse_log.py /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0005/caffe.INFO /project/focus/abby/tc_tripletloss/models/logs/traffickcam/lr0005/

# once we determine a good learning rate, update the solver to use 'train.prototxt' instead of 'overtrain.prototxt'
# train, storing log information
GLOG_log_dir=/project/focus/abby/tc_tripletloss/models/logs/traffickcam/ $CAFFE_ROOT/build/tools/caffe train -solver /project/focus/abby/tc_tripletloss/models/solver.prototxt -weights /project/focus/abby/tc_tripletloss/models/alexnet_places365.caffemodel -gpu 0
# parse logs
$CAFFE_ROOT/tools/extra/parse_log.py /project/focus/abby/tc_tripletloss/models/logs/traffickcam/caffe.INFO /project/focus/abby/tc_tripletloss/models/logs/traffickcam/
