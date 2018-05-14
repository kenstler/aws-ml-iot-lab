# AWS ML & IoT Lab

The goal of these labs is to test two different configurations for integrating ML and IoT devices. The application is to track crowd emotions in real-time.

## Challenge 1

Deploy pre-trained model to an inference endpoint using SageMaker and user-configured inference code. Your endpoint will process raw images, detect faces if present, push face crops to an S3 bucket, and return raw detection coordinates to requester.

## Challenge 2

You will configure an IoT device to process images at specified intervals and send them to the SageMaker endpoint deployed in Challenge 1. This will be done by configuring GreenGrass on the device, and writing a custum lambda function to process images from your devices camera. 

You will also configure a cloud-side lambda function that will trigger when faces are written to the S3 bucket from the previous step. This function will process faces through Rekognition, collect emotion scores, push the metrics to Cloudwatch for tracking, and save results to a DynamoDB table.

## Challenge 3

Rather than run inference in the cloud using SageMaker, we'll use DeepLens to run inferene on the edge and push face crops to S3 from the edge devie itself. Here you will register a DeepLens device and push a custom configured inference lambda wth a face detection model down to the device.

# To -do
* Provide step-by-step instructions (re:screenshots) for every stage of this lab.
* Incude instructons for ensuring users have assigned the right permission policies to the roles used at each step of the way.
