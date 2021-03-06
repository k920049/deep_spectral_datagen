
import numpy as np
import os
import sys
import caffe
from os import listdir
from os.path import isfile, join

'''
Initialization of network,
init_net(gpu_id, network_name)

'''


def init_net(model_dir=None, gpu_id=None):

    if gpu_id is None:
        gpu_id = 0

    if(gpu_id > 1):
        print('GPU id out of bounds, set to 0')
        gpu_id = 0

    print('GPU id used: ', gpu_id)

    if(model_dir is None):
        # these are hardcoded for now
        model_dir = './caffe_models/chirp3f/'

    if model_dir[-1] != '/':
        model_dir = model_dir + '/'

    # read in mean image, should be same for all classifiers
    mean_filename = model_dir + 'mean.binaryproto'
    proto_data = open(mean_filename, "rb").read()
    a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
    mean = caffe.io.blobproto_to_array(a)[0]

    # pretrained model and prototxt def
    onlyfiles = [f for f in listdir(model_dir) if isfile(join(model_dir, f))]

    fname = ''
    for i in range(len(onlyfiles)):
        if(onlyfiles[i].split('.')[1].lower() == 'caffemodel'):
            fname = onlyfiles[i]
            break

    pretrained_model = model_dir + fname
    model_def = model_dir + 'deploy.prototxt'

    # these are typical
    #channel_swap = [0]
    image_dims = [256, 256]
    input_scale = 1.0
    raw_scale = 255.0

    caffe.set_mode_gpu()
    caffe.set_device(gpu_id)

    # Make classifier.
    classifier = caffe.Classifier(model_def, pretrained_model,
                                  image_dims=image_dims, mean=mean,
                                  input_scale=input_scale, raw_scale=raw_scale)

    print('Network load from ' + fname)
    return(classifier)


'''
Forward pass through pre-defined classifier network
Input is an image file (.jpg, .png)
Defaults to non center-only processing
Ex:  labels, predictions = net_process(classifier, input_file, center_only)
'''


def net_process(classifier, input_file, center_only=None):

    # center only =1 does center crop only
    # center only =0 does crops and mirrors of input
    if center_only is None:
        center_only = 1

    input_file = os.path.expanduser(input_file)

    try:
        inputs = [caffe.io.load_image(input_file, False)]
    except:
        print("Input image file not found!")
        return -1

    #print("Classifying %d inputs." % len(inputs))

    # Classify.
    #start = time.time()
    predictions = classifier.predict(inputs, center_only)
    #print("Done in %.2f s." % (time.time() - start))

    return predictions
