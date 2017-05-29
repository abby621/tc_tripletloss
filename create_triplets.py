import csv
import numpy as np
import random
import os

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

# RANDOM
classes_0_ind = {}
for ix in range(0,len(classes)):
    classes_0_ind[classes[ix]] = ix

allTriplets = []
for cls in classes:
    print cls
    class_0_ind = classes_0_ind[cls]
    posInds = np.where(allClasses==int(cls))[0]
    negInds = np.where(allClasses!=int(cls))[0]
    if len(posInds) > 1:
        for ix in range(0,len(posInds)):
            anchorIm = allIms[posInds[ix]]
            # pick a positive example from the possible positive examples
            possiblePosInds = [aa for aa in range(len(posInds)) if aa != ix]
            random.shuffle(possiblePosInds)
            for iy in range(min(10,len(possiblePosInds))):
                posInd = posInds[possiblePosInds[iy]]
                positiveIm = allIms[posInd]
                # pick a negative example from the possible negative examples
                negInd = random.choice(negInds)
                negativeIm = allIms[negInd]
                negativeImClass = allClasses[negInd]
                negativeImClass_0_ind = classes_0_ind[str(negativeImClass)]
                # add this triplet to our list of all triplets
                allTriplets.append((anchorIm, str(class_0_ind), positiveIm, str(class_0_ind), negativeIm, str(negativeImClass_0_ind)))

randomOrder = range(len(allTriplets))
random.shuffle(randomOrder)
shuffledTriplets = [allTriplets[aa] for aa in randomOrder]

batchSize = 600
assert batchSize % 3 == 0

testTriplets = allTriplets[:batchSize*4]
# grab everything else as train triplets, but make sure it's divisible by 3
trainTriplets = allTriplets[batchSize*4+1:len(allTriplets)-len(allTriplets[batchSize*4+1:])%3]

smallTestTriplets = allTriplets[:batchSize]
smallTrainTriplets = allTriplets[batchSize+1:batchSize*2]

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
