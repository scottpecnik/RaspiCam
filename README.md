# RaspiCam
Python program for the Raspberry Pi.  Takes pictures based on an interval for a timelapse.

Pictures are stored in Cloudant in IBM's bluemix.

# Building Time Lapse
Time lapse is built by running DownloadPictures.py and getting all pics local.

ffmpeg is used to convert to a video:
```
./ffmpeg -r 25 -i ~/Desktop/pictures/%03d.png ~/Desktop/cat.mp4
```