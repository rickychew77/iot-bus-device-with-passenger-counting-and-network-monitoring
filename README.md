# IOT BUS DEVICE WITH PASSENGER COUNTING AND NETWORK MONITORING
Develop a device using Raspberry Pi with Intel Movidius Neural Compute Stick to perform deep learning inference on gender and age prediction, at the same time perform network peformance monitoring.

There will be 2 modules in this project:
1) Passenger Counting
  face_detector.py are mainly using algorithm of centroid tracking, referred from Adrian Rosebruck in Pyimagesearch, to perform face detection and then cropping the region of interest (ROI) in order to feed them into GenderNet and AgeNet.
  GenderNet and AgeNet from Intel Movidius NCS example (/workspace/ncappzoo/caffe) are used as reference and changed some of the code for my project purposes in python file name (genderrun.py and agerun.py).
  
2) Network Monitoring
  Network performance metrics like ping, download speed (ms), upload speed (ms) are acquired through this device as well. These information will then sent to Google Drive at self-defined time period using crontab and gdrive. 
  

Note: These code in this repository is not fully written by me, it is done through some cross referencing from different sources as stated above to fulfill my project requirement. 
