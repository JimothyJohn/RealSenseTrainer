## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

#####################################################
##              Align Depth to Color               ##
#####################################################

# First import the library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2, argparse, os

WINDOW = True

parser = argparse.ArgumentParser(description='Object name')
parser.add_argument('path', help='training object')
args = parser.parse_args()

# Create a pipeline
pipeline = rs.pipeline()

#Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams
# Can also set to 1280x720@6
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

# We will be removing the background of objects more than
#  clipping_distance_in_meters meters away
clipping_distance_in_meters = 1 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)

# imageList = int(sorted(os.listdir(args.path+'/2D-data/'))[-1][4:9])
currentFiles = sorted(os.listdir('{}/2D-data/'.format(args.path)))
if len(currentFiles) > 0:
    fileIndex = int(currentFiles[-1][4:9])+1
else:
    fileIndex = 1

# Streaming loop
try:
    while fileIndex > 0:
        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Find closest point to the camera
        minDepth = np.min(depth_image[np.nonzero(depth_image)])

        # Remove background - Set pixels further than clipping_distance to grey
        grey_color = 153
        maskImage = np.where((depth_image > minDepth*1.2) | (depth_image <= 0), 0, 255)
        
        # warm up time
        np.savetxt('{}/3D-data/depth_{:05d}.csv'.format(
            args.path,fileIndex), depth_image, delimiter=",")
        cv2.imwrite('{}/2D-data/img_{:05d}.png'.format(
            args.path,fileIndex),color_image)
        cv2.imwrite('{}/labels/seg_{:05d}.png'.format(
            args.path,fileIndex),maskImage)
        
        fileIndex += 1
        # Render images
        if WINDOW:
            depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
            bg_removed = np.where((depth_image_3d > minDepth*1.2) | (depth_image_3d <= 0), grey_color, color_image)
            cv2.namedWindow('Align Example', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('Align Example', bg_removed)

        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()
