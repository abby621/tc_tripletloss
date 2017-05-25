import csv
import numpy as np
import random

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

batchSize = 30
tripletSize = batchSize/3

allBatches = []
for cls in classes:
    print cls
    class_0_ind = classes_0_ind[cls]
    posInds = np.where(allClasses==int(cls))[0]
    negInds = np.where(allClasses!=int(cls))[0]
    if len(posInds) > 1:
        for ix in range(0,len(posInds)):
            thisBatch = []
            anchorIm = allIms[posInds[ix]]
            thesePosInds = [aa for aa in range(len(posInds)) if aa != ix]
            posIndsToUse = random.sample(thesePosInds,min(len(thesePosInds),10))
            while len(posIndsToUse) < 10:
                posIndsToUse.append(random.choice(thesePosInds))
            for posInd in posIndsToUse:
                positiveIm = allIms[posInd]
                negInd = random.choice(negInds)
                negativeIm = allIms[negInd]
                negativeImClass = allClasses[negInd]
                negativeImClass_0_ind = classes_0_ind[str(negativeImClass)]
                thisBatch.append((anchorIm, str(class_0_ind), positiveIm, str(class_0_ind), negativeIm, str(negativeImClass_0_ind)))
#                     new_triplet_file.write('%s,%s,%s,%s,%s,%s\n' % (anchorIm, str(class_0_ind), positiveIm, str(class_0_ind), negativeIm, str(negativeImClass_0_ind)))
            allBatches.append(thisBatch)

random.shuffle(allBatches)

testBatches = allBatches[:1000]
trainBatches = allBatches[1001:101001]

smallTestBatches = allBatches[:100]
smallTrainBatches = allBatches[101:201]

def write_triplet_file(batches,file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    txt_file = open(file_path,'a')
    for batch in batches:
        anchorIms = []
        positiveIms = []
        negativeIms = []
        for triplet in batch:
            anchorIms.append((triplet[0],triplet[1]))
            positiveIms.append((triplet[2],triplet[3]))
            negativeIms.append((triplet[4],triplet[5]))
        for a in anchorIms:
            txt_file.write('%s %s\n' % (a[0],a[1]))
        for p in positiveIms:
            txt_file.write('%s %s\n' % (p[0],p[1]))
        for n in negativeIms:
            txt_file.write('%s %s\n' % (n[0],n[1]))
    txt_file.close()

write_triplet_file(trainBatches,'/project/focus/datasets/tc_tripletloss/train_triplets.txt')
write_triplet_file(testBatches,'/project/focus/datasets/tc_tripletloss/test_triplets.txt')
write_triplet_file(smallTrainBatches,'/project/focus/datasets/tc_tripletloss/small_train_triplets.txt')
write_triplet_file(smallTestBatches,'/project/focus/datasets/tc_tripletloss/small_test_triplets.txt')
