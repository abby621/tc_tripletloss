import csv
import numpy as np
import random
import os

# =========== if we need to compute features, start here, else jump down ====================
import caffe
import cv2
from caffe.io import blobproto_to_array
from caffe.proto import caffe_pb2

def getFeats(ims,net,feat_layer):
    net.blobs['data'].reshape(len(ims),3,227,227)
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_mean('data', IM_MEAN)
    transformer.set_transpose('data', (2,0,1))
    transformer.set_channel_swap('data', (2,1,0))
    transformer.set_raw_scale('data', 255.0)
    caffe_input = np.empty((len(ims),3,227,227))
    for ix in range(len(ims)):
        caffe_input[ix,:,:,:] = transformer.preprocess('data',caffe.io.load_image(ims[ix]))
    net.blobs['data'].data[...] = caffe_input
    out = net.forward()
    feat = net.blobs[feat_layer].data.copy()
    return feat

caffe.set_device(0)
caffe.set_mode_gpu()

net_model = '/project/focus/abby/tc_tripletloss/models/deploy/deploy.prototxt'
net_weights = '/project/focus/abby/tc_tripletloss/models/alexnet_places365.caffemodel'
net = caffe.Net(net_model, net_weights,caffe.TEST)

blob = caffe_pb2.BlobProto()
data = open('/project/focus/datasets/tc_tripletloss/mean.binaryproto', 'rb' ).read()
blob.ParseFromString(data)
arr = np.array(blobproto_to_array(blob))
IM_MEAN = arr.squeeze()

im_file = '/project/focus/datasets/tc_tripletloss/triplet_train_roomsonly.txt'
with open(im_file,'rU') as f:
    rd = csv.reader(f,delimiter=' ')
    im_list = list(rd)

ims_by_class = {}
for i in im_list:
    if not i[1] in ims_by_class:
        ims_by_class[i[1]] = []
    ims_by_class[i[1]].append(i[0])

classes = ims_by_class.keys()
numClasses = len(classes)

allClasses = np.zeros((len(im_list)),dtype='int')
allIms = []
startInd = 0
for cls in classes:
    allClasses[startInd:startInd+len(ims_by_class[cls])] = int(cls)
    allIms.extend(ims_by_class[cls])
    startInd += len(ims_by_class[cls])

# hack to make sure we have batches of 100, this is dumb
while len(allIms)%100 != 0:
    allClasses = np.append(allClasses,int(cls))
    allIms.append(ims_by_class[cls][0])

# RANDOM
classes_0_ind = {}
for ix in range(0,len(classes)):
    classes_0_ind[classes[ix]] = ix

allFeats = np.empty((len(allIms),365))
inds = range(0,len(allIms),100)
ctr = 0
for ind in inds:
    print ctr, ' of ', len(inds)
    ims = allIms[ind:ind+100]
    feat = getFeats(ims,net,'fc8')
    allFeats[ind:ind+100,:] = feat.squeeze()
    ctr += 1

np.save('/project/focus/abby/tc_tripletloss/classes.npy',allClasses)
np.save('/project/focus/abby/tc_tripletloss/ims.npy',np.asarray(allIms))
np.save('/project/focus/abby/tc_tripletloss/feats.npy',allFeats)
np.save('/project/focus/abby/tc_tripletloss/classes_0_ind.npy',classes_0_ind)

# =========== if we loaded from files, start here:
def getDist(feat,otherFeat):
    dist = (otherFeat - feat)**2
    dist = np.sum(dist)
    dist = np.sqrt(dist)
    return dist

allClasses = np.load('/project/focus/abby/tc_tripletloss/classes.npy')
allIms = np.load('/project/focus/abby/tc_tripletloss/ims.npy')
allFeats = np.load('/project/focus/abby/tc_tripletloss/feats.npy')
classes_0_ind = np.load('/project/focus/abby/tc_tripletloss/classes_0_ind.npy').item()
classes = classes_0_ind.keys()

allTriplets = []
for cls in classes:
    print cls
    class_0_ind = classes_0_ind[cls]
    posInds = np.where(allClasses==int(cls))[0]
    negInds = np.where(allClasses!=int(cls))[0]
    if len(posInds) > 1:
        for ix in range(0,len(posInds)):
            anchorIm = allIms[posInds[ix]]
            anchorFeat = allFeats[posInds[ix]]
            # pick a positive example from the possible positive examples
            possiblePosInds = [aa for aa in range(len(posInds)) if allIms[posInds[aa]] != anchorIm]
            theseTriplets = []
            ctr = 0
            while ctr < len(possiblePosInds) and len(theseTriplets) <= 10:
                posInd = posInds[possiblePosInds[ctr]]
                positiveIm = allIms[posInd]
                positiveFeat = allFeats[posInd]
                posDist = getDist(anchorFeat,positiveFeat)
                if posDist < 32:
                    # pick a negative example from the possible negative examples
                    negDist = 1000000
                    tries = 0
                    while negDist > posDist and tries < 100:
                        tries += 1
                        negInd = random.choice(negInds)
                        negFeat = allFeats[negInd]
                        negDist = getDist(anchorFeat,negFeat)
                        if negDist <= posDist:
                            negativeIm = allIms[negInd]
                            negativeImClass = allClasses[negInd]
                            negativeImClass_0_ind = classes_0_ind[str(negativeImClass)]
                            # add this triplet to our list of all triplets
                            theseTriplets.append((anchorIm, str(class_0_ind), positiveIm, str(class_0_ind), negativeIm, str(negativeImClass_0_ind)))
                ctr += 1
            allTriplets.extend(theseTriplets)

randomOrder = range(len(allTriplets))
random.shuffle(randomOrder)
shuffledTriplets = [allTriplets[aa] for aa in randomOrder]

batchSize = 600
assert batchSize % 3 == 0

testTriplets = shuffledTriplets[:batchSize*4]
# grab everything else as train triplets, but make sure it's divisible by 3
trainTriplets = shuffledTriplets[batchSize*4+1:len(shuffledTriplets)-len(shuffledTriplets[batchSize*4+1:])%3]

smallTestTriplets = shuffledTriplets[:batchSize]
smallTrainTriplets = shuffledTriplets[batchSize+1:batchSize*2]

def write_triplet_file(triplets,batchSize,filePath):
    if os.path.exists(filePath):
        os.remove(filePath)
    txtFile = open(filePath,'a')
    for ix in range(0,len(triplets),batchSize):
        anchorIms = []
        positiveIms = []
        negativeIms = []
        batch = triplets[ix:ix+batchSize/3]
        for triplet in batch:
            anchorIms.append((triplet[0],triplet[1]))
            positiveIms.append((triplet[2],triplet[3]))
            negativeIms.append((triplet[4],triplet[5]))
        for a in anchorIms:
            txtFile.write('%s %s\n' % (a[0],a[1]))
        for p in positiveIms:
            txtFile.write('%s %s\n' % (p[0],p[1]))
        for n in negativeIms:
            txtFile.write('%s %s\n' % (n[0],n[1]))
    txtFile.close()

write_triplet_file(trainTriplets,batchSize,'/project/focus/datasets/tc_tripletloss/train_triplets.txt')
write_triplet_file(testTriplets,batchSize,'/project/focus/datasets/tc_tripletloss/test_triplets.txt')
write_triplet_file(smallTrainTriplets,batchSize,'/project/focus/datasets/tc_tripletloss/small_train_triplets.txt')
write_triplet_file(smallTestTriplets,batchSize,'/project/focus/datasets/tc_tripletloss/small_test_triplets.txt')
