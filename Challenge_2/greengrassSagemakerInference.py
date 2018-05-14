#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

# greengrassSagemakerInference.py

import greengrasssdk
import platform
from threading import Timer
import time
import boto3
import cv2

# Creating a greengrass core sdk client
client = greengrasssdk.client('iot-data')


def greengrassSagemakerInference_run():
    vidcap=cv2.VideoCapture(0)
    vidcap.open(0)
    #sleep(1) this may be required if camera needs warm up.
    retval, image = vidcap.read()
    vidcap.release()
    endpoint_name = 'xxxxx'
    runtime = boto3.Session().client(service_name='sagemaker-sagemaker',region_name='us-east-1')
    #payload = bytearray(image) this may be necessary, need to test if inference doesn't work
    response = runtime.invoke_endpoint(EndpointName=endpoint_name, ContentType='application/x-image', Body=image)
    client.publish(topic='ModelInference', payload=response)

    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(5, greengrassSagemakerInference_run).start()


# Execute the function above
greengrassSagemakerInference_run()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return
