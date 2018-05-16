# DataPalooza: A Music Festival themed ML + IoT Workshop

Welcome to DataPalooza! 

In this workshop, you play the role of data scientists working for a bold new startup tasked with providing a new type of EDM music festival experience. You and your team aim to leverage Machine Learning and IoT to come up with a connected experience for both fans and artists alike by building a **Crowd Emotion Tracking Application**. Your application will provide real-time insights into the crowd response at different stages; this enables fans to find stages with the best performances, and artists to monitor crowd response to their setlist, adjusting if necessary.

To build this application, you will use AWS services such as Amazon SageMaker, Amazon S3, Amazon Rekognition, Amazon CloudWatch, Amazon DynamoDB, AWS Lambda, AWS GreenGrass, and AWS DeepLens. You will explore two common ML/IoT configurations for running inference: hosting inference in the cloud with C5, and hosting inference on the edge with DeepLens.

## [Challenge 1](https://github.com/kenstler/aws-ml-iot-lab/tree/master/Challenge_1)

In this challenge, you will deploy a pre-trained face-detection model to a SageMaker endpoint. Your endpoint will process raw images, detect faces if present, push face crops to an S3 bucket, and return raw detection coordinates to requester.

## [Challenge 2](https://github.com/kenstler/aws-ml-iot-lab/tree/master/Challenge_1)

You will configure an IoT device to process images at specified intervals and send them to the SageMaker endpoint deployed in Challenge 1. This will be done by configuring GreenGrass on the device, and writing a custum lambda function to process images from your devices camera. 

You will also configure a cloud-side lambda function that will trigger when faces are written to the S3 bucket from the previous step. This function will process faces through Rekognition, collect emotion scores, push the metrics to Cloudwatch for tracking, and save results to a DynamoDB table.

## [Challenge 3](https://github.com/kenstler/aws-ml-iot-lab/tree/master/Challenge_1)

Rather than run inference in the cloud using SageMaker, we'll use DeepLens to run inferene on the edge and push face crops to S3 from the edge devie itself. Here you will register a DeepLens device and push a custom configured inference lambda wth a face detection model down to the device.

# To -do
* Provide step-by-step instructions (re:screenshots) for every stage of this lab.
* Incude instructons for ensuring users have assigned the right permission policies to the roles used at each step of the way.
