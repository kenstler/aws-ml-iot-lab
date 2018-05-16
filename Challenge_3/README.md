# Challenge 3: Edge Inference Pipeline
## Summary

Now that we've successfully built out a pipeline for our application based around cloud-inference, it's time to revisit this configuration. In ML/IoT pipelines, we often have a choice to make about where inference is ran. Recall that in this particular scenario, the face detection inference is acting as a gate to the Rekognition API call:
* Only trigger when a face is detected
* Only actually send the face crop

In the previous Challenge, we cited performance and speed as two advantages of cloud inference. Unfortunately, by keeping inference in the crowd our IoT devices must regularly send images at constant intervals (i.e. they're **always on**) and they send entire images. This seems like a waste of bandwidth; by putting face-detection inference at the edge, we can directly make Rekognition calls from the device itself. The tradeoff here is that while we're only sending face crops when there detected over the network, inference at the edge can be less performant.

In this challenge, you will swap out the ML/IoT part of the previous pipeline with a new pipeline that uses AWS DeepLens to run inference on the edge. DeepLens will then put face crops to the S3 bucket correctly, continuing the rest of the application pipeline.

* Step-by-step instructions (re:screenshots)
* Instructions on re-setting and registering DeepLens
* configure inference lambda for edge inference w/ S3 bucket
* Deploy lambda, model as a DeepLens Project to device
