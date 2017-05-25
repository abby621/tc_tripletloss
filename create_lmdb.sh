rm -r /project/focus/datasets/tc_tripletloss/small_triplet_test_lmdb
$CAFFE_ROOT/build/tools/convert_imageset --resize_height 227 --resize_width 227 / /project/focus/datasets/tc_tripletloss/small_test_triplets.txt /project/focus/datasets/tc_tripletloss/small_triplet_test_lmdb
rm -r /project/focus/datasets/tc_tripletloss/small_triplet_train_lmdb
$CAFFE_ROOT/build/tools/convert_imageset --resize_height 227 --resize_width 227 / /project/focus/datasets/tc_tripletloss/small_train_triplets.txt /project/focus/datasets/tc_tripletloss/small_triplet_train_lmdb
rm -r /project/focus/datasets/tc_tripletloss/triplet_test_lmdb
$CAFFE_ROOT/build/tools/convert_imageset --resize_height 227 --resize_width 227 / /project/focus/datasets/tc_tripletloss/test_triplets.txt /project/focus/datasets/tc_tripletloss/triplet_test_lmdb
rm -r /project/focus/datasets/tc_tripletloss/triplet_train_lmdb
$CAFFE_ROOT/build/tools/convert_imageset --resize_height 227 --resize_width 227 / /project/focus/datasets/tc_tripletloss/train_triplets.txt /project/focus/datasets/tc_tripletloss/triplet_train_lmdb
