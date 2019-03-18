# IOT Bus Device with passenger counting and network monitoring
This project is to develop a device using Raspberry Pi with 2 Intel Movidius Neural Compute Stick to perform deep learning inference on gender and age prediction, at the same time perform network peformance monitoring.

There will be 2 modules in this project:
1) Passenger Counting - face_detector.py are mainly using algorithm of centroid tracking, referred from Adrian Rosebruck in Pyimagesearch, to perform face detection and then cropping the region of interest (ROI) in order to feed them into GenderNet and AgeNet.GenderNet and AgeNet from Intel Movidius NCS example (/workspace/ncappzoo/caffe) are used as reference and I've changed some of the code to suit my project in python file named genderrun.py and agerun.py.
  
2) Network Monitoring - Network performance metrics like ping (ms), download speed (Mbit/s), upload speed (Mbit/s) are acquired through this device as well. These information will then sent to Google Drive at self-defined time period using crontab and gdrive. 
  
The automation of the the Google Drive sync is done by crontab.

Note: These code in this repository is not fully written by me, it is done through some cross referencing from different sources as stated above to fulfill my project requirement. The whole project is meant to run on Raspberry Pi (I am using Raspberry Pi 3 B), please get yourself short USB male to female extension to fit the Movidius Neural Compute Stick as their size big enough to physically blocking the other USB port of the Rasp.
