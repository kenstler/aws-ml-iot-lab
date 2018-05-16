# DataPalooza: A Music Festival themed ML + IoT Workshop

Welcome to DataPalooza! 

In this workshop, you play the role of data scientists working for a bold new startup tasked with providing a new type of EDM music festival experience. You and your team aim to leverage Machine Learning and IoT to come up with a connected experience for both fans and artists alike by building a **Crowd Emotion Tracking Application**. Your application will provide real-time insights into the crowd response at different stages; this enables fans to find stages with the best performances, and artists to monitor crowd response to their setlist, adjusting if necessary.

To build this application, you will use AWS services such as Amazon SageMaker, Amazon S3, Amazon Rekognition, Amazon CloudWatch, Amazon DynamoDB, AWS Lambda, AWS GreenGrass, and AWS DeepLens. You will explore two common ML/IoT configurations for running inference: hosting inference in the cloud with C5, and hosting inference on the edge with DeepLens.

## [Challenge 1](https://github.com/kenstler/aws-ml-iot-lab/tree/master/Challenge_1)

The first stop in the pipeline of your Crowd Emotion Tracking App is a face-detection model. We'll be using Rekognition to detect face emotions. Rather than sending a stream of raw images to Rekognition, we're going to pre-process images with the face-detection model to:

Only send images to Rekognition when a face is detected
Only send the actual face crop itself
This limits both the number of API calls we make, as well as the size of content we send.

In this challenge, you will use SageMaker in your efforts to deploy a face-detection model. You will first launch a SageMaker notebook instance; from your notebook, you will be able to explore the data your model will train on, see how the model is trained, and deploy a pre-trained model to an inference endpoint. You will also create an S3 bucket for the endpoint to store detected faces, which you will need as part of your app's pipeline.

## [Challenge 2](https://github.com/kenstler/aws-ml-iot-lab/tree/master/Challenge_1)

You will configure an IoT device to process images at specified intervals and send them to the SageMaker endpoint deployed in Challenge 1. This will be done by configuring GreenGrass on the device, and writing a custum lambda function to process images from your devices camera. 

You will also configure a cloud-side lambda function that will trigger when faces are written to the S3 bucket from the previous step. This function will process faces through Rekognition, collect emotion scores, push the metrics to Cloudwatch for tracking, and save results to a DynamoDB table.

## [Challenge 3](https://github.com/kenstler/aws-ml-iot-lab/tree/master/Challenge_1)

Rather than run inference in the cloud using SageMaker, we'll use DeepLens to run inferene on the edge and push face crops to S3 from the edge devie itself. Here you will register a DeepLens device and push a custom configured inference lambda wth a face detection model down to the device.

# To -do
* Provide step-by-step instructions (re:screenshots) for every stage of this lab.
* Incude instructons for ensuring users have assigned the right permission policies to the roles used at each step of the way.
