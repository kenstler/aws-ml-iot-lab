# DataPalooza: A Music Festival themed ML + IoT Workshop

Welcome to DataPalooza! 

In this workshop, you play the role of data scientists working for a bold new startup tasked with providing a new type of EDM music festival experience. You and your team aim to leverage Machine Learning and IoT to come up with a connected experience for both fans and artists alike by building a **Crowd Emotion Tracking Application**. Your application will provide real-time insights into the crowd response at different stages; this enables fans to find stages with the best performances, and artists to monitor crowd response to their setlist, adjusting if necessary.

To build this application, you will use AWS services such as Amazon SageMaker, Amazon S3, Amazon Rekognition, Amazon CloudWatch, Amazon DynamoDB, AWS Lambda, AWS GreenGrass, and AWS DeepLens. You will explore two common ML/IoT configurations for running inference: hosting inference in the cloud with C5, and hosting inference on the edge with DeepLens.

## [Prep Exercise](https://github.com/kenstler/aws-ml-iot-lab/tree/master/Challenge_1)

The first stop in the pipeline of your Crowd Emotion Tracking App is a face-detection model. We'll be using Rekognition to detect face emotions. Rather than sending a stream of raw images to Rekognition, we're going to pre-process images with the face-detection model to:
* Only send images to Rekognition when a face is detected
* Only send the actual face crop itself

This limits both the number of API calls we make, as well as the size of content we send.

In this challenge, you will use SageMaker in your efforts to deploy a face-detection model. You will first launch a SageMaker notebook instance; from your notebook, you will be able to explore the data your model will train on, see how the model is trained, and deploy a pre-trained model to an inference endpoint. You will also create an S3 bucket for the endpoint to store detected faces, which you will need as part of your app's pipeline.

## [Challenge 1](https://github.com/kenstler/aws-ml-iot-lab/tree/master/Challenge_2)
Now that you have a face-detection model on a SageMaker endpoint, we can leverage that endpoint to build out an ML/IoT pipeline for our app that does all the inference in the cloud. By running inference in the cloud, we're able to use accurate models at a rapid pace by leveraging powerful computational instances like C5.

In this challenge, you will configure an IoT device to act as a smart camera, which will send images to the endpoint for face-detection. You'll build out the rest of the pipeline necessary to create a dashboard for tracking crowd emotions in real-time, including AWS Lambda, Amazon DynamoDB, Amazon Rekognition, and Amazon CloudWatch.

## [Challenge 2](https://github.com/kenstler/aws-ml-iot-lab/tree/master/Challenge_3)

Now that we've successfully built out a pipeline for our application based around cloud-inference, it's time to revisit this configuration. In ML/IoT pipelines, we often have a choice to make about where inference is ran. Recall that in this particular scenario, the face detection inference is acting as a gate to the Rekognition API call:
* Only trigger when a face is detected
* Only actually send the face crop

In the previous Challenge, we cited performance and speed as two advantages of cloud inference. Unfortunately, by keeping inference in the cloud our IoT devices must regularly send images at constant intervals (i.e. they're **always on**) and they send entire images. This seems like a waste of bandwidth; by putting face-detection inference at the edge, we can directly make Rekognition calls from the device itself. The tradeoff here is that while we're only sending face crops when they're detected over the network, inference at the edge can be less performant.

In this challenge, you will swap out the ML/IoT part of the previous pipeline with a new pipeline that uses AWS DeepLens to run inference on the edge. DeepLens will then put face crops to the S3 bucket correctly, continuing the rest of the application pipeline.

# To -do
* Mahendra, insert your isntructions in the field provided for Challenge 1
* DeepLens registration instructions link for Challenge 2
