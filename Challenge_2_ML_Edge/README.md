# Challenge 2: ML at the Edge
## Summary

Now that we've successfully built out a pipeline for our application based around cloud-inference, it's time to revisit this configuration. In ML/IoT pipelines, we often have a choice to make about where inference is ran. Recall that in this particular scenario, the face detection inference is acting as a gate to the Rekognition API call:
* Only trigger when a face is detected
* Only actually send the face crop

In the previous Challenge, we cited performance and speed as two advantages of cloud inference. Unfortunately, by keeping inference in the cloud our IoT devices must regularly send images at constant intervals (i.e. they're **always on**) and they send entire images. This seems like a waste of bandwidth; by putting face-detection inference at the edge, we can directly make Rekognition calls from the device itself. The tradeoff here is that while we're only sending face crops when there detected over the network, inference at the edge can be less performant.

In this challenge, you will swap out the ML/IoT part of the previous pipeline with a new pipeline that uses AWS DeepLens to run inference on the edge. DeepLens will then put face crops to the S3 bucket correctly, continuing the rest of the application pipeline.

* Step-by-step instructions (re:screenshots)
* Instructions on re-setting and registering DeepLens
* configure inference lambda for edge inference w/ S3 bucket
* Deploy lambda, model as a DeepLens Project to device

## Instructions

### AWS DeepLens Registration

[Instructions on registering DeepLens can be found here.](https://s3.amazonaws.com/deeplens-workshop-06-20-2018/MLGGDeepLensWorkshop06-20-2018.pdf)

### Create DeepLens Lambda

Now that you've registered your DeepLens device, it's time to create a custom project that we can deploy to the device to run face-detection and push crops to S3.

A DeepLens **Project** consists of two things:
* A model artifact: This is the model that is used for inference.
* A Lambda function: This is the script that runs inference on the device.

Before we deploy a project to DeepLens, we need to create a custom lambda function that will use the face-detection model on the device to detect faces and push crops to S3.

You will repeat the steps in Challenge 2 where you created a Lambda function from the "greengrass-hello-world" blueprint. This time, however, you will select "Choose an existing role" and then select "AWSDeepLensLambdaRole". 

![Alt text](../screenshots/deeplens_lambda_0.png)

Next, you will replace the default function with the inference-lambda.py script under Challenge_3, which we've included here for you:

**Note**: Be sure to replace "your-bucket" with the name of the bucket you've been using thus far.

```python
#
# Copyright Amazon AWS DeepLens, 2017
#

import os
import sys
import datetime
import greengrasssdk
from threading import Timer
import time
import awscam
import cv2
from threading import Thread
import urllib
import zipfile

#boto3 is not installed on device by default.

boto_dir = '/tmp/boto_dir'
if not os.path.exists(boto_dir):
    os.mkdir(boto_dir)
urllib.urlretrieve("https://s3.amazonaws.com/dear-demo/boto_3_dist.zip", "/tmp/boto_3_dist.zip")
with zipfile.ZipFile("/tmp/boto_3_dist.zip", "r") as zip_ref:
    zip_ref.extractall(boto_dir)
sys.path.append(boto_dir)

import boto3

# Creating a greengrass core sdk client
client = greengrasssdk.client('iot-data')

# The information exchanged between IoT and clould has
# a topic and a message body.
# This is the topic that this code uses to send messages to cloud
iotTopic = '$aws/things/{}/infer'.format(os.environ['AWS_IOT_THING_NAME'])

ret, frame = awscam.getLastFrame()
ret, jpeg = cv2.imencode('.jpg', frame)

Write_To_FIFO = True

class FIFO_Thread(Thread):
    def __init__(self):
        ''' Constructor. '''
        Thread.__init__(self)

    def run(self):
        fifo_path = "/tmp/results.mjpeg"
        if not os.path.exists(fifo_path):
            os.mkfifo(fifo_path)
        f = open(fifo_path, 'w')
        client.publish(topic=iotTopic, payload="Opened Pipe")
        while Write_To_FIFO:
            try:
                f.write(jpeg.tobytes())
            except IOError as e:
                continue

def push_to_s3(img, index):
    try:
        bucket_name = "your-bucket"

        timestamp = int(time.time())
        now = datetime.datetime.now()
        key = "faces/{}_{}/{}_{}/{}_{}.jpg".format(now.month, now.day,
                                                   now.hour, now.minute,
                                                   timestamp, index)

        s3 = boto3.client('s3')

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        _, jpg_data = cv2.imencode('.jpg', img, encode_param)
        response = s3.put_object(ACL='public-read',
                                 Body=jpg_data.tostring(),
                                 Bucket=bucket_name,
                                 Key=key)

        client.publish(topic=iotTopic, payload="Response: {}".format(response))
        client.publish(topic=iotTopic, payload="Face pushed to S3")
    except Exception as e:
        msg = "Pushing to S3 failed: " + str(e)
        client.publish(topic=iotTopic, payload=msg)

def greengrass_infinite_infer_run():
    try:
        modelPath = "/opt/awscam/artifacts/mxnet_deploy_ssd_FP16_FUSED.xml"
        modelType = "ssd"
        input_width = 300
        input_height = 300
        prob_thresh = 0.25
        results_thread = FIFO_Thread()
        results_thread.start()

        # Send a starting message to IoT console
        client.publish(topic=iotTopic, payload="Face detection starts now")

        # Load model to GPU (use {"GPU": 0} for CPU)
        mcfg = {"GPU": 1}
        model = awscam.Model(modelPath, mcfg)
        client.publish(topic=iotTopic, payload="Model loaded")
        ret, frame = awscam.getLastFrame()
        if ret == False:
            raise Exception("Failed to get frame from the stream")

        yscale = float(frame.shape[0]/input_height)
        xscale = float(frame.shape[1]/input_width)

        doInfer = True
        while doInfer:
            # Get a frame from the video stream
            ret, frame = awscam.getLastFrame()
            # Raise an exception if failing to get a frame
            if ret == False:
                raise Exception("Failed to get frame from the stream")

            # Resize frame to fit model input requirement
            frameResize = cv2.resize(frame, (input_width, input_height))

            # Run model inference on the resized frame
            inferOutput = model.doInference(frameResize)

            # Output inference result to the fifo file so it can be viewed with mplayer
            parsed_results = model.parseResult(modelType, inferOutput)['ssd']
            # client.publish(topic=iotTopic, payload = json.dumps(parsed_results))
            label = '{'
            for i, obj in enumerate(parsed_results):
                if obj['prob'] < prob_thresh:
                    break
                offset = 25
                xmin = int( xscale * obj['xmin'] ) + int((obj['xmin'] - input_width/2) + input_width/2)
                ymin = int( yscale * obj['ymin'] )
                xmax = int( xscale * obj['xmax'] ) + int((obj['xmax'] - input_width/2) + input_width/2)
                ymax = int( yscale * obj['ymax'] )

                crop_img = frame[ymin:ymax, xmin:xmax]

                push_to_s3(crop_img, i)

                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 165, 20), 4)
                label += '"{}": {:.2f},'.format(str(obj['label']), obj['prob'] )
                label_show = '{}: {:.2f}'.format(str(obj['label']), obj['prob'] )
                cv2.putText(frame, label_show, (xmin, ymin-15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 165, 20), 4)
            label += '"null": 0.0'
            label += '}'
            client.publish(topic=iotTopic, payload=label)
            global jpeg
            ret, jpeg = cv2.imencode('.jpg', frame)

    except Exception as e:
        msg = "Test failed: " + str(e)
        client.publish(topic=iotTopic, payload=msg)

    # Asynchronously schedule this function to be run again in 15 seconds
    Timer(15, greengrass_infinite_infer_run).start()


# Execute the function above
greengrass_infinite_infer_run()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return
```

Once you've copied and pasted the code, click "Save" as before, and this time you'll also click "Actions" and then "Publish new version".

![Alt text](../screenshots/deeplens_lambda_1.png)

Then, enter a brief description and click "Publish."

![Alt text](../screenshots/deeplens_lambda_2.png)

Before we can run this lambda on the device, we need to attach the right permissions to the right roles. While we assigned a role to this lambda, "AWSDeepLensLambdaRole", it's only a placeholder. Lambda's deployed through greengrass actually inherit their policy through a greengrass group role.

Similar to what we did in challenge 2, we need to add permissions to this role for the lambda function to access S3. To do this, go to the IAM dashboard, find the "AWSDeepLensGreenGrassGroupRole", and attach the policy "AmazonS3FullAccess". If you've forgotten how to do this, please refer to Challenge 2 as an example.

### Create & Deploy DeepLens Project

With the lambda created, we can now make a project using it and the built-in face detection model.

From the DeepLens homepage dashboard, select "Projects" from the left side-bar:

![Alt text](../screenshots/deeplens_project_0.png)

Then select "Create new project"

![Alt text](../screenshots/deeplens_project_1.png)

Next, select "Create a new blank project" then click "Next".

![Alt text](../screenshots/deeplens_project_2.png)

Now, name your deeplens project.

![Alt text](../screenshots/deeplens_project_3.png)

Next, select "Add model". From the pop-up window, select "deeplens-face-detection" then click "Add model".

![Alt text](../screenshots/deeplens_project_4.png)

Next, select "Add function". from the pop-up window, select your deeplens lambda function and click "Add function".

![Alt text](../screenshots/deeplens_project_5.png)

Finally, click "Create".

![Alt text](../screenshots/deeplens_project_6.png)

Now that the project has been created, you will select your project from the project dashboard and click "Deploy to device".

![Alt text](../screenshots/deeplens_project_7.png)

Select the device you're deploying too, then click "Review" (your screen will look different here).

![Alt text](../screenshots/deeplens_project_8.png)

Finally, click "Deploy" on the next screen to begin project deployment.

![Alt text](../screenshots/deeplens_project_9.png)

You should now start to see deployment status. Once the project has been deployed, your deeplens will now start processing frames and running face-detection locally. When faces are detected, it will push to your S3 bucket. Everything else in the pipeline remains the same, so return to your dashboard to see the new results coming in!

**Note**: If your model download progress hangs at a blank state (Not 0%, but **blank**) then you may need to reset greengrass on DeepLens. To do this, log onto the DeepLens device, open up a terminal, and type the following command:
`sudo systemctl restart greengrassd.service --no-block`. After a couple minutes, you model should start to download.
