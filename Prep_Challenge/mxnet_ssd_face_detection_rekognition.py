from __future__ import absolute_import
import mxnet as mx
import random
import datetime
import json
import time
import numpy as np
import boto3
import urllib

urllib.urlretrieve ("https://raw.githubusercontent.com/drj11/pypng/master/code/png.py", "png.py")
import png

###############################
###     Hosting Code        ###
###############################

def push_to_s3(img, index):
    bucket_name = "your-bucket"

    timestamp = int(time.time())
    now = datetime.datetime.now()
    key = "faces/{}_{}/{}_{}/{}_{}.jpg".format(now.month, now.day,
                                               now.hour, now.minute,
                                               timestamp, index)

    s3 = boto3.client('s3')

    png.from_array(img.astype(np.uint8), 'RGB').save('img.png')
    response = s3.put_object(ACL='public-read',
                         Body=open('img.png', 'rb'),
                         Bucket=bucket_name,
                         Key=key)

def model_fn(model_dir):
    sym, arg_params, aux_params = mx.model.load_checkpoint('%s/model/deploy_ssd' % model_dir, 0)
    net = mx.mod.Module(sym, label_names=None)
    net.bind(data_shapes=[('data', (1, 3, 300, 300))])
    net.set_params(arg_params, aux_params)
    return net

def transform_fn(net, data, input_content_type, output_content_type):
    img = np.array(json.loads(data))
    batch = mx.io.DataBatch([mx.nd.array(np.expand_dims(np.transpose(img, (2, 0, 1)), 0))])
    net.forward(batch)
    dets = net.get_outputs()[0].asnumpy()
    response_body = json.dumps(dets.tolist()[0])
    height = img.shape[0]
    width = img.shape[1]
    colors = dict()
    dets = dets[0]
    for i in range(dets.shape[0]):
        cls_id = int(dets[i, 0])
        if cls_id >= 0:
            score = dets[i, 1]
            if score > 0.5:
                if cls_id not in colors:
                    colors[cls_id] = (random.random(), random.random(), random.random())
                xmin = int(dets[i, 2] * width)
                ymin = int(dets[i, 3] * height)
                xmax = int(dets[i, 4] * width)
                ymax = int(dets[i, 5] * height)
                crop_img = img[ymin:ymax, xmin:xmax]
                push_to_s3(crop_img, i)            
    return response_body, output_content_type
    