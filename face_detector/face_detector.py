from mvnc import mvncapi as mvnc
from pyimagesearch.centroidtracker import CentroidTracker
from imutils.video import VideoStream
from imutils.video import FPS
from time import localtime, strftime

import numpy as np
import argparse
import imutils
import time
import cv2
import os

#initialize the class of object to be detected
CLASS_PERSON = 15

# frame dimensions should be sqaure
PREPROCESS_DIMS = (300, 300)
DISPLAY_DIMS = (900, 900)

# calculate the multiplier needed to scale the bounding boxes
DISP_MULTIPLIER = DISPLAY_DIMS[0] // PREPROCESS_DIMS[0]

# Detection threshold: Minumum confidance to tag as valid detection
CONFIDANCE_THRESHOLD = 0.60 #60% confidant

def preprocess_image(input_image):
	# preprocess the image
	preprocessed = cv2.resize(input_image, PREPROCESS_DIMS)
	preprocessed = preprocessed - 127.5
	preprocessed = preprocessed * 0.007843
	preprocessed = preprocessed.astype(np.float16)

	# return the image to the calling function
	return preprocessed

def predict(image, graph):
	# preprocess the image
	image = preprocess_image(image)

	# send the image to the NCS and run a forward pass to grab the
	# network predictions
	graph.LoadTensor(image.astype(np.float16), 'user object')
	output, userobj = graph.GetResult()
	#print (output)
	rects = []
       	
# ---- Deserialize the output from an SSD based network ----
# @param output The NCS returns a list/array in this structure:
# First float16: Number of detections
# Next 6 values: Unused
# Next consecutive batch of 7 values: Detection values
#   0: Image ID (always 0)
#   1: Class ID (index into labels.txt)
#   2: Detection score
#   3: Box left coordinate (x1) - scaled value between 0 & 1
#   4: Box top coordinate (y1) - scaled value between 0 & 1
#   5: Box right coordinate (x2) - scaled value between 0 & 1
#   6: Box bottom coordinate (y2) - scaled value between 0 & 1

        # Dictionary where the deserialized output will be stored
    	output_dict = {}

    	# Extract the original image's shape
    	height, width, channel = frame.shape

    	# Total number of detections
    	output_dict['num_detections'] = int( output[0] )

    	# Variable to track number of valid detections
    	valid_detections = 0
        
	for detection in range( output_dict['num_detections'] ):

        	# Skip the first 7 values, and point to the next batch of 7 values
        	base_index = 7 + ( 7 * detection )

        	# Record only those detections whose confidance meets our threshold
                if( output[ base_index + 2 ] > args['confidence']  ) :

            		output_dict['detection_classes_' + str(valid_detections)] = \
                	int( output[base_index + 1] )
                            
            		output_dict['detection_scores_' + str(valid_detections)] = \
                	int( output[base_index + 2] * 100 )

            		x = [ ( output[base_index + 3]  ), 
            			( output[base_index + 5]  ) ]

            		y = [ ( output[base_index + 4]  ), 
            		 	( output[base_index + 6]  ) ] 

            		output_dict['detection_boxes_' + str(valid_detections)] = \
            		    list( zip( y, x ) )

            		valid_detections += 1


			# compute the (x, y)-coordinates of the bounding box for
			# the object, then update the bounding box rectangles list
			x1 = x[0]
			x2 = x[1]
			y1 = y[0]
			y2 = y[1]

                        box = (x1, y1, x2, y2) * np.array([width,height,width,height])
			#print (box)
                        rects.append(box.astype(int))
                        print (rects)
			(startX, startY, endX, endY) = box.astype("int")
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				(0, 255, 0), 2)

	# update our centroid tracker using the computed set of bounding
        # box rectangles
        objects = ct.update(rects)
        
	path = '/home/pi/Desktop/face_detector/capture/'
        if (int (output[base_index + 1 ]) == CLASS_PERSON ): 
        	for i in rects:
                	xx,yy,ww,hh = [v for v in i ]
                        print (xx)
                        print (yy)
                        print (ww)
                        print (hh)
                        roi=frame[yy:yy+hh,xx:xx+ww]
			for (objectID, centroid) in objects.items():
                                
                                text  = 'ID{}'.format(objectID)
	                        #text = 'ID' + str(idx)
                                cur_time = strftime ( "%Y_%m_%d_%H_%M_%S", localtime() )
        	                cv2.imwrite(os.path.join(path,text + '.jpg'),roi)
                                #cv2.imwrite(os.path.join(path, 'face_' + str(objectID) + '.jpg'), roi)
                	        print (text + ' at ' +  cur_time)
                                with open ('passenger.csv', 'a') as passenger:
                                    passenger.write('\n' + cur_time + '\t' + text)

	return ()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-g", "--graph", 
        default="mobilenetgraph",
	help="path to input graph file")
ap.add_argument("-c", "--confidence", default=.6,
	help="confidence threshold")
ap.add_argument("-d", "--display", type=int, default=0,
	help="switch to display image on screen")
args = vars(ap.parse_args())

# grab a list of all NCS devices plugged in to USB
print("[INFO] finding NCS devices...")
devices = mvnc.EnumerateDevices()

# if no devices found, exit the script
if len(devices) == 0:
	print("[INFO] No devices found. Please plug in a NCS")
	quit()

# use the first device since this is a simple test script
# (you'll want to modify this is using multiple NCS devices)
print("[INFO] found {} devices. device0 will be used. "
	"opening device0...".format(len(devices)))
device = mvnc.Device(devices[0])
device.OpenDevice()

# open the CNN graph file
print("[INFO] loading the graph file into RPi memory...")
with open(args["graph"], mode="rb") as f:
	graph_in_memory = f.read()

# load the graph into the NCS
print("[INFO] allocating the graph on the NCS...")
graph = device.AllocateGraph(graph_in_memory)

# initialize our centroid tracker and frame dimensions
ct = CentroidTracker()
(H, W) = (None, None)

# open a pointer to the video stream thread and allow the buffer to
# start to fill, then start the FPS counter
print("[INFO] starting the video stream and FPS counter...")
vs = VideoStream(src=0).start()
time.sleep(1)
fps = FPS().start()


# loop over the frames from the video stream
while True:
    try:
	# read the next frame from the video stream and resize it
	frame = vs.read()
	frame = imutils.resize(frame, width=400)
	# use the NCS to acquire predictions
	predict(frame, graph)

	# update the FPS counter
	fps.update()
    
    except KeyboardInterrupt:
        break
# stop the FPS counter timer
fps.stop()

# destroy all windows if we are displaying them
if args["display"] > 0:
	cv2.destroyAllWindows()

# stop the video stream
vs.stop()

# clean up the graph and device
graph.DeallocateGraph()
device.CloseDevice()

# display FPS information
print("\n===============================================")
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

