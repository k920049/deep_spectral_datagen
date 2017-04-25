from os import listdir
from os.path import isfile, join
import chirp_class as cc
import numpy as np
import matplotlib.pyplot as plt
import cv2

def false_alarm_tst(fdir=None, mdir=None, ftype=None):

    pngfiles=[]

    if fdir is None:
        mypath = './'
    else:
        mypath = fdir

    if(ftype is None):
        ftype = 'png'

    if(mdir is None):
        mdir ='./'

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    cclass = cc.init_net(model_dir=mdir)

    for i in xrange(len(onlyfiles)):
        if(onlyfiles[i].split('.')[-1].lower() == ftype.lower()  ):
            pngfiles.append(onlyfiles[i])

    print 'Processing ' + str(len(pngfiles)) + ' files from ' + mypath
    prob = np.zeros(  (len(pngfiles),2)  )
    fa = 0
    N = len(pngfiles)
    plt.ion()

    for i in xrange(N):
        prob[i,:] = cc.net_process(cclass, join(mypath,pngfiles[i]), 0)

        #all files should be negatives, check which ones are not
        if( prob[i,0] < prob[i,1] ):  # class 0 is neg, class 1 is pos
            fa=fa+1
            print 'File ' + pngfiles[i] + ' triggered,  neg=' + str(np.round(10*prob[i,0])/10) + ', pos=' + str(np.round(10*prob[i,1])/10) + ', False alarm rate: ' + str(fa) + '/' + str(N)
#            plt.figure()
#            img = cv2.imread(join(mypath,pngfiles[i]))
#            plt.imshow(img)
#            plt.title(pngfiles[i])

    print 'Final PFA: ' + str(fa*1.0/N*100) + '%'


def detection_tst(fdir=None, mdir=None, ftype=None):

    pngfiles=[]

    if fdir is None:
        mypath = './'
    else:
        mypath = fdir

    if(ftype is None):
        ftype = 'png'

    if(mdir is None):
        mdir ='./'

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    cclass = cc.init_net(model_dir=mdir)

    for i in xrange(len(onlyfiles)):
        if(onlyfiles[i].split('.')[-1].lower() == ftype.lower()  ):
            pngfiles.append(onlyfiles[i])

    print 'Processing ' + str(len(pngfiles)) + ' files from ' + mypath
    prob = np.zeros(  (len(pngfiles),2)  )
    miss = 0
    N = len(pngfiles)
    plt.ion()

    for i in xrange(N):
        prob[i,:] = cc.net_process(cclass, join(mypath,pngfiles[i]), True)

        #all files should be positives, check which ones are not
        if( prob[i,0] > prob[i,1] ):  # class 0 is neg, class 1 is pos
            miss=miss+1
            print 'File ' + pngfiles[i] + ' triggered,  neg=' + str(np.round(10*prob[i,0])/10) + ', pos=' + str(np.round(10*prob[i,1])/10) + ', Miss rate: ' + str(miss) + '/' + str(N)
#            plt.figure()
#            img = cv2.imread(join(mypath,pngfiles[i]))
#            plt.imshow(img)
#            plt.title(pngfiles[i])

    pmiss = miss*1.0/N

    print 'Final PD: ' + str((1-pmiss) * 100)+'%, Pmiss: ' + str(pmiss * 100) + '%'
