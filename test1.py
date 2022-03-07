import sys
from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview(fullscreen=False, window=(100,200,480,640))
sleep(10)
camera.stop_preview()
